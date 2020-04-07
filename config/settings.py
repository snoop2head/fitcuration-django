"""
For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# utilizing sentry to monitor errors
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


# Build paths to the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("FITCURATION_SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
LOCAL = bool(os.environ.get("LOCAL"))
if LOCAL:
    DEBUG = True
else:
    DEBUG = False


ALLOWED_HOSTS = [
    ".elasticbeanstalk.com",
    "localhost",
    "0401fitcuration-dev.ap-northeast-2.elasticbeanstalk.com",
    "172.31.37.6",
    "127.0.0.1",
]

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Letting Django know installed thrid party apps
THIRD_PARTY_APPS = ["django_countries", "storages"]

# Letting Django know my established Project apps by stating here.
# Importing apps.py in each apps: core, users, rooms, reviews ...
PROJECT_APPS = [
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "results.apps.ResultsConfig",
    "lists_carousels.apps.ListsCarouselsConfig",
    "exercises.apps.ExercisesConfig",
    "locations.apps.LocationsConfig",
    "categories.apps.CategoriesConfig",
]


# Installed apps are applications that django looks at
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],  # where to look for templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = "/static/"

# adding path for static files as http://127.0.0.1:8000/static/css/styles.css
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = "users.User"

# https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-MEDIA_ROOT
# storing photos in ./uploads
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

# https://docs.djangoproject.com/en/3.0/ref/settings/#media-url
# previously, link to image was http://127.0.0.1:8000/admin/rooms/photo/9/change/room_photos/photoname.png
# now, changing the link to image as http://127.0.0.1:8000/media/photoname.png
MEDIA_URL = "/media/"  # "/media" slash / in fronth means absolute

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if LOCAL is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

else:
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_URL"),
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )

    # staticfile storage
    STATICFILES_STORAGE = "config.custom_storages.StaticStorage"
    DEFAULT_FILE_STORAGE = "config.custom_storages.UploadStorage"

    # https://console.aws.amazon.com/iam/home?region=ap-northeast-2#/security_credentials
    AWS_S3_REGION_NAME = "ap-northeast-2"
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = "fitcuration-noopy-static-bucket-korea"
    AWS_AUTO_CREATE_BUCKET = True
    AWS_BUCKET_ACL = "public-read"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

    # https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-HOST
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": os.environ.get("RDS_HOST"),
            "NAME": os.environ.get("RDS_NAME"),
            "USER": os.environ.get("RDS_USER"),
            "PASSWORD": os.environ.get("RDS_DBPW"),
            "PORT": "5432",
        }
    }


# Email Configuration
# https://docs.djangoproject.com/en/3.0/topics/email/#quick-example
EMAIL_HOST = "smtp.mailgun.org"
EMAIL_PORT = "587"

# getting system variables from .env
EMAIL_HOST_USER = os.environ.get("MAILGUN_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("MAILGUN_PASSWORD")
# print(EMAIL_HOST_PASSWORD)
EMAIL_FROM = "no-reply@sandbox969376d0bd8e48d69ed51fc305cdd23d.mailgun.org"
