import os
from pathlib import Path
from datetime import timedelta
from decouple import config



BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "corsheaders",
    "storages",

    # Local apps
    "members",
    "departments",
    "contents",
    "messaging",
    "admin_panel",
    # "accounts",
    # "gmail_service",
    # "calendar_service",
    # "drive_service",
    # "tasks_service",
    # "voice_service",
    # "browser_automation",
    # "agent_core",
    # "utils",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware", 
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database (SQLite for now — you will later move to Postgres)
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {
            "sslmode": "require",
        },
        "NAME": "neondb",
        "USER": "neondb_owner",
        "PASSWORD": "npg_aLlqXE91kxPp",
        "HOST": "ep-spring-leaf-ae3t9084-pooler.c-2.us-east-2.aws.neon.tech",
        "PORT": "5432",
    }
}


# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}


# JWT Config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# AUTH_USER_MODEL = "accounts.User"
# config/settings.py
AUTH_USER_MODEL = "members.Member"


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"

# drf-spectacular settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Believer's Website API",
    "DESCRIPTION": "API documentation for Believer's Website",
    "VERSION": "1.0.0",
    # Optional: add server entries or auth schemes as needed
}

# CORS
CORS_ALLOW_ALL_ORIGINS = True



EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)

FRONTEND_URL = config("FRONTEND_URL", default="http://localhost:3000")


# Backblaze B2 S3-compatible storage
AWS_ACCESS_KEY_ID = config("B2_KEY_ID")       # Your B2 Key ID
AWS_SECRET_ACCESS_KEY = config("B2_APP_KEY")  # Your B2 Application Key
AWS_STORAGE_BUCKET_NAME ="bgministries"     # Your B2 bucket
AWS_S3_ENDPOINT_URL = "https://s3.us-east-005.backblazeb2.com"  # Your B2 endpoint
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}
AWS_DEFAULT_ACL = None  # Optional: recommended for modern B2
AWS_QUERYSTRING_AUTH = False  # Make URLs public
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_REGION_NAME = "us-east-005"  # Your B2 bucket region

# Tell Django to use B2 for media

MEDIA_URL = "/media/"  # logical URL; storage backend will generate the real URL




STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "endpoint_url": AWS_S3_ENDPOINT_URL,
            "region_name": AWS_S3_REGION_NAME,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

