"""
Django settings for backend project.
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = (
    os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []
)

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.staticfiles",
    "Product",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS — environment-driven.
#
# In development set CORS_ALLOW_ALL_ORIGINS=True in .env for convenience.
# In production, leave that unset (defaults False) and list every allowed
# frontend origin in CORS_ALLOWED_ORIGINS, comma-separated, e.g.:
#   CORS_ALLOWED_ORIGINS=https://app.example.com,https://admin.example.com
_cors_allow_all = os.getenv("CORS_ALLOW_ALL_ORIGINS", "False").strip().lower() == "true"
CORS_ALLOW_ALL_ORIGINS = _cors_allow_all

if not CORS_ALLOW_ALL_ORIGINS:
    _raw_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]


ROOT_URLCONF = "django_app.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "django_app.wsgi.application"

DATABASES = {}

import mongoengine

# Use a separate test database when running tests.
# This prevents integration tests from touching real data.
# "test" is always in sys.argv when running: python manage.py test
IS_TESTING = "test" in sys.argv

MONGO_DB_NAME = os.getenv("MONGO_DB")
TEST_MONGO_DB_NAME = os.getenv("MONGO_TEST_DB", f"{MONGO_DB_NAME}_test")

mongoengine.connect(
    db=TEST_MONGO_DB_NAME if IS_TESTING else MONGO_DB_NAME,
    host=os.getenv("MONGO_HOST"),
    port=int(os.getenv("MONGO_PORT")),
    username=os.getenv("MONGO_USERNAME"),
    password=os.getenv("MONGO_PASSWORD"),
    authentication_source=os.getenv("MONGO_AUTH_SOURCE", "admin"),
)

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"