from django import forms
from . import models

# UserCreationForm: https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.forms.UserCreationForm
# from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "이메일"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )

    def clean(self):
        # get the email data that user sent to us, clean data
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # try to find matching email object in Users database
        try:
            user = models.User.objects.get(email=email)
            # check_password(): https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.check_password
            # check_password() is encrypting password, and if the encrypted password is saved on the database
            if user.check_password(password):
                # always return cleaned data
                return self.cleaned_data
            else:
                # adding error on password field with error form
                self.add_error("password", forms.ValidationError("Wrong Password"))

        # if user's email object does not exist in db, add error
        # adding error on email field which prevents reaching to views.py LoginView Post request
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User Does Not Exists"))


# using ModelForm to reduce repetetive scripting for fields
# https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#modelform
class SignUpForm(forms.ModelForm):
    class Meta:
        # fetch model from User app
        model = models.User
        # INPUT FIELDS FOR THE USERS TO PUT IN WHEN SIGNUP
        fields = ("email",)

        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "이메일"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "전에 등록하신 이메일 계정입니다. 로그인해주세요!", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    # cleaning password_again(field for confirmation)
    def clean_password_again(self):
        # get cleaned data from template
        password = self.cleaned_data.get("password")
        password_again = self.cleaned_data.get("password_again")
        # if fetched password doesn't match password again then raise validation error.
        if password != password_again:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            # return password to database
            return password

    # ModelForm has save method: https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#the-save-method
    def save(self, *args, **kwargs):
        # Additional interception is taken place with commit=False: create object but don't put it in database
        user = super().save(commit=False)
        # email and password from the form
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        # username field of user app
        user.username = email
        # hashing password with set_password: https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.User.set_password
        user.set_password(password)
        user.save()
