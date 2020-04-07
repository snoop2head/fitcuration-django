# importing settings.py file of django project
from django.conf import settings

# Utilizing Django's AbstractUser class
from django.contrib.auth.models import AbstractUser
from django.db import models

# email verification
# send_mail function from django: https://docs.djangoproject.com/en/3.0/topics/email/#quick-example
from django.core.mail import send_mail

# strip html tags from string
from django.utils.html import strip_tags

# import html from templates folder, render it to use as string
from django.template.loader import render_to_string

# random verification_key generator for email verification
import uuid

# customized manager from core app
from core import managers as core_managers


class User(AbstractUser):
    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    # Three types of (user registration -> account verification -> login)
    REGISTER_LOGIN_EMAIL = "email"
    REGISTER_LOGIN_GITHUB = "github"
    REGISTER_LOGIN_KAKAO = "kakao"

    REGISTER_LOGIN_METHOD = (
        (REGISTER_LOGIN_EMAIL, "Email"),
        (REGISTER_LOGIN_GITHUB, "Github"),
        (REGISTER_LOGIN_KAKAO, "Kakao"),
    )

    # null is for the database, and blank is for forms on website
    # null means "empty values are acceptable", and blank also means the same.
    avatar = models.ImageField(blank=True)

    # charfield: text field with limit of single line
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    # Adding column(field) to database with empty

    # textfield: text field without limit
    bio = models.TextField(default="", blank=True)
    # bio = models.TextField(null=True) # Or, empty cell in field is accepted

    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    # currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True)

    # boolean field is true of false
    # superhost = models.BooleanField(default=False)

    # three types of verification method(email, kakao, github) added on database
    register_login_method = models.CharField(
        max_length=50, choices=REGISTER_LOGIN_METHOD, default=REGISTER_LOGIN_EMAIL
    )

    # email fields added to models.py
    # emailing with django
    email_confirmed = models.BooleanField(default=False)
    # randomly generated numbers for email confirmation
    email_verification_key = models.CharField(max_length=20, default="", blank=True)

    objects = core_managers.CustomUserManager()

    # ------------------- end of the database fields -------------------------------

    # email verification method connected with ./views.py
    def verify_email(self):
        if self.email_confirmed is False:
            # using python random generator uuid library, generate random verification key
            # result is form of tuple, needs to be indexed like list
            verification_key = uuid.uuid4().hex[:20]
            # save random verification key to the field
            self.email_verification_key = verification_key
            # importing html message from static template, render it to string and use it to send_mail
            html_message = render_to_string(
                "emails/verify_email.html",
                context={"verification_key": verification_key},
            )
            # send email using django's send_email function: https://docs.djangoproject.com/en/3.0/topics/email/#quick-example
            # for specific arguments for the function, refer here: https://docs.djangoproject.com/en/3.0/topics/email/#send-mail
            send_mail(
                # email title
                "Verify FitCuration Account",
                # email content without html tags
                strip_tags(html_message),
                # email sender setted up in settings.py as no-reply
                settings.EMAIL_FROM,
                # recipient_list
                [self.email],
                # not raising error even if it failed, or raise
                fail_silently=False,
                # html
                html_message=html_message,
            )
            # saving verification_key to user's email_verification_key field
            self.save()
            return
