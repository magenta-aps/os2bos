"""
Django settings for bevillingsplatform project.

Generated by "django-admin startproject" using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import configparser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
base_settings_path = os.path.join(BASE_DIR, "base.ini")

# define defaults for ConfigParser
defaults = {"BASE_DIR": BASE_DIR}
config = configparser.ConfigParser(defaults=defaults)
# load base settings from base.ini into the ConfigParser
config.read(base_settings_path)

# If another settings ini is defined, load it
settings_name = os.getenv("DJANGO_SETTINGS_INI", None)
if settings_name:  # pragma: no branch
    settings_path = os.path.join(BASE_DIR, settings_name)
    config.read(settings_path)

# use settings section as default
default_config = config["settings"]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = default_config.get("SECRET_KEY")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = default_config.getboolean("DEBUG")

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_extensions",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bevillingsplatform.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "bevillingsplatform.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": default_config.get("DATABASE_ENGINE"),
        "NAME": default_config.get("DATABASE_NAME"),
        "USER": default_config.get("DATABASE_USER"),
        "PASSWORD": default_config.get("DATABASE_PASSWORD"),
        "HOST": default_config.get("DATABASE_HOST"),
        "PORT": default_config.get("DATABASE_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator"
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "da-dk"

TIME_ZONE = "Europe/Copenhagen"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

FORCE_SCRIPT_NAME = "/api"
STATIC_URL = FORCE_SCRIPT_NAME + "/static/"
STATIC_ROOT = default_config.get("STATIC_ROOT")

# Serviceplatform service UUIDs
SERVICEPLATFORM_UUIDS = {
    "service_agreement": default_config.get(
        "SERVICEPLATFORM_SERVICE_AGREEMENT"
    ),
    "user_system": default_config.get("SERVICEPLATFORM_USER_SYSTEM"),
    "user": default_config.get("SERVICEPLATFORM_USER"),
    "service": default_config.get("SERVICEPLATFORM_SERVICE")
}

# Serviceplatform Certificate

SERVICEPLATFORM_CERTIFICATE_PATH = default_config.get("SERVICEPLATFORM_CERTIFICATE_PATH")
