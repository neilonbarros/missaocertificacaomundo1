import os
from pathlib import Path

from django.contrib.messages import constants as messages
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        "environments",
        ".env",
    )
)


SECRET_KEY = os.getenv(
    key="DJANGO_SECRET_KEY",
    default=None,
)
if SECRET_KEY is None:
    raise RuntimeError("without DJANGO_SECRET_KEY")

ALLOWED_HOSTS = str(
    os.getenv(
        key="DJANGO_ALLOWED_HOSTS",
        default="",
    )
).split(",")

INTERNAL_IPS = ALLOWED_HOSTS

DEBUG = (
    True
    if os.getenv(
        key="DJANGO_DEBUG",
        default="0",
    )
    == "1"
    else False
)


INSTALLED_APPS = [
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #
    #
    "app",
]

DEBUG_TOOLBAR = (
    True
    if os.getenv(
        key="DJANGO_DEBUG_TOOLBAR",
        default="0",
    )
    == "1"
    else False
)

if DEBUG_TOOLBAR is True:
    INSTALLED_APPS += [  # noqa
        "debug_toolbar",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                # "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "global/static/")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "global/media/")


LANGUAGE_CODE = "pt-br"

LANGUAGES = (
    ("pt-br", "Português"),
    ("en", "English"),
)

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "app" / "locale",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary DEBUG",
    messages.INFO: "alert-primary INFO",
    messages.SUCCESS: "alert-success SUCCESS",
    messages.WARNING: "alert-warning WARNING",
    messages.ERROR: "alert-danger ERROR",
}
