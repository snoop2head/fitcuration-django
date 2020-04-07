from django.shortcuts import redirect, reverse

# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.edit/FormView/
from django.views.generic import FormView

# reverse_lazy to prevent circular import
from django.urls import reverse_lazy

# https://docs.djangoproject.com/en/3.0/topics/auth/default/#authenticating-users
from django.contrib.auth import authenticate, login, logout

# import users app's login forms and models
from . import forms, models
import os
import requests

main_domain = os.environ.get("MAIN_DOMAIN")


class LoginView(FormView):

    """ Login View """

    # Using inherited FormView class instead of LoginView: https://ccbv.co.uk/projects/Django/3.0/django.views.generic.edit/FormView/
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    """
    # function based view for post request
    def post(self, request):
        form = forms.LoginForm(request.POST)
        # print(form)

        # print(form.is_valid())
        if form.is_valid():
            # cleaned data is the cleaned result of all fields
            # print(form.cleaned_data)
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})
    """


# Logout function: https://docs.djangoproject.com/en/3.0/topics/auth/default/#how-to-log-a-user-out
# LogoutView class: https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.views.LogoutView
def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    # Using inherited FormView class: https://ccbv.co.uk/projects/Django/3.0/django.views.generic.edit/FormView/
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    # intially providing an example to users for signup
    # initial = {
    #     "first_name": "길동",
    #     "last_name": "홍",
    #     "email": "honggildong@gmail.com",
    # }

    # to see where "form" came from, CMD + Click on FormView inherited class
    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        # getting function from models.py users app, verify user by sending randomly genearated string
        user.verify_email()
        return super().form_valid(form)


# completing verification process when user clicks href at his/her email
def complete_verification(request, verification_key):
    print(verification_key)
    # if designated verification key matches verification key given through views.py, proceed.
    try:
        # get queryset matching designated random email verification key from models.py
        user = models.User.objects.get(email_verification_key=verification_key)
        # changing a single user queryset object's boolean field email_confirmed from False to True
        user.email_confirmed = True
        # since user is verified, empty a single user queryset object's email_verification charfield.
        user.email_verification_key = ""
        # save information on database
        user.save()
    # if designated verification key does not match verification key given through views.py, raise error.
    except models.User.DoesNotExist:
        # to do : add error message
        pass
    # redirecting to home when successful
    return redirect(reverse("core:home"))


# https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/
def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = main_domain + "users/login/github/callback"
    # get request to github: https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/#1-request-a-users-github-identity
    # check for parameter arguments like scope of user action: https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


# action encountering github exception is descriped at the end of github_callback()
# replacing return redirect(reverse("core:home"))
class GithubException(Exception):
    pass


def github_callback(request):
    try:
        # id and password to request to github
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        # print(request.GET)
        # <QueryDict: {'code': ['123921039102adf']}>
        github_callback_code = request.GET.get("code")
        if github_callback_code is not None:
            # post request to github api
            # https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/#2-users-are-redirected-back-to-your-site-by-github
            token_request_to_github = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={github_callback_code}",
                # getting response which is in json format
                headers={"Accept": "application/json"},
            )
            # accepting json response from github
            token_response_json = token_request_to_github.json()
            error = token_response_json.get("error", None)  # default=None
            if error is not None:
                # return redirect(reverse("core:home"))
                raise GithubException()
            else:
                # requesting to github api
                # https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/#3-use-the-access-token-to-access-the-api
                access_token = token_response_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                # response from github api: profile information
                profile_info_json = profile_request.json()
                github_username = profile_info_json.get("login", None)

                # if user is validated from github api then get name, email and bio information
                if github_username is not None:
                    github_name = profile_info_json.get("name")
                    github_email = profile_info_json.get("email")
                    github_bio = profile_info_json.get("bio")

                    # if there is user in database == email received from github, login the user
                    try:
                        # lookup user information on database
                        user_in_db = models.User.objects.get(email=github_email)
                        # if user's registered method isn't github
                        if (
                            user_in_db.register_login_method
                            != models.User.REGISTER_LOGIN_GITHUB
                        ):
                            # user didn't registered in github, but trying to log in to github -> raise error
                            raise GithubException()
                        else:
                            # proceed log in with github method
                            # login user at the end of the day
                            login(request, user_in_db)

                    # if user does not exist in database, register the user
                    except models.User.DoesNotExist:
                        # create queryset object in database with username, first_name, bio, email, register_login_method fields
                        new_user_to_db = models.User.objects.create(
                            username=github_email,
                            first_name=github_name,
                            bio=github_bio,
                            email=github_email,
                            register_login_method=models.User.REGISTER_LOGIN_GITHUB,
                            email_confirmed=True,
                        )
                        # https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.User.set_unusable_password
                        new_user_to_db.set_unusable_password()
                        new_user_to_db.save()
                        # after user is saved to db, login the user
                        login(request, new_user_to_db)

                    # redirect to home at the end of the day
                    return redirect(reverse("core:home"))

                # if user does not exist in github api response, redirect to login panel
                else:
                    raise GithubException()
        else:
            raise GithubException()
    # whatever error happens, redirect to login panel
    except GithubException:
        return redirect(reverse("users:login"))


# https://developers.kakao.com/docs/restapi/user-management
def kakao_login(request):
    app_rest_api_key = os.environ.get("KAKAO_REST_API_KEY")
    redirect_uri = main_domain + "users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


# https://developers.kakao.com/docs/restapi/user-management
def kakao_callback(request):
    try:
        app_rest_api_key = os.environ.get("KAKAO_REST_API_KEY")
        redirect_uri = main_domain + "users/login/kakao/callback"
        user_token = request.GET.get("code")
        # post request
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
        )

        token_response_json = token_request.json()
        error = token_response_json.get("error", None)
        # if there is an error from token_request
        if error is not None:
            raise KakaoException()
        access_token = token_response_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        # print(profile_json)
        # parsing profile json
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException()
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        profile_image_url = profile.get("profile_image_url")
        try:
            user_in_db = models.User.objects.get(email=email)
            if user_in_db.register_login_method != models.User.REGISTER_LOGIN_KAKAO:
                raise KakaoException()
            else:
                login(request, user_in_db)
        except models.User.DoesNotExist:
            new_user_to_db = models.User.objects.create(
                username=email,
                email=email,
                first_name=nickname,
                register_login_method=models.User.REGISTER_LOGIN_KAKAO,
                email_confirmed=True,
            )
            # https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.User.set_unusable_password
            new_user_to_db.set_unusable_password()
            new_user_to_db.save()
            # after user is saved to db, login the user
            login(request, new_user_to_db)
        return redirect(reverse("core:home"))
    except KakaoException:
        return redirect(reverse("users:login"))
