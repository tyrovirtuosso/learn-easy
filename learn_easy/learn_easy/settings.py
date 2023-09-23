from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-is336lyl-##0jdl3)-2^h*dik=vxc!=2$m99)_u7_5%m3do^j*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS =  ['localhost', '127.0.0.1', 'example.com']



# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Django Extensions
    "django_extensions",
    # Custom Apps
    "usersApp.apps.UsersappConfig",
    "items.apps.ItemsConfig",
    "decks.apps.DecksConfig",
    # Django Channels
    "channels",
    # allauth app
    "django.contrib.sites",
    "allauth", 
    "allauth.account",
    "allauth.socialaccount", 
    # allauth social providers
    "allauth.socialaccount.providers.github", 
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.twitter_oauth2",
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware"
]

ROOT_URLCONF = "learn_easy.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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

WSGI_APPLICATION = "learn_easy.wsgi.application"

# social_app/settings.py
AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",
)
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_FORMS = {'signup': 'usersApp.forms.CustomSignupForm'}
SOCIALACCOUNT_FORMS = {'signup': 'usersApp.forms.SocialCustomSignupForm',}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1 
ACCOUNT_ADAPTER = 'usersApp.adapters.CustomAccountAdapter'

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': os.environ.get('GITHUB_OAUTH_CLIENT_ID'),
            'secret': os.environ.get('GITHUB_OAUTH_CLIENT_SECRET'),
            'key': ''
        }
    },
    'twitter_oauth2': {
        'APP': {
            'client_id': os.environ.get('TWITTER_OAUTH_CLIENT_ID'),
            'secret': os.environ.get('TWITTER_OAUTH_CLIENT_SECRET'),
            'key': ''
        }
    },
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
    
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#     BASE_DIR / "static"
# ]
STATIC_ROOT = BASE_DIR.parent / "local-cdn" / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "usersApp.CustomUser"
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"


CHANNEL_LAYERS = {
    # 'default': {'BACKEND': 'channels_redis.core.RedisChannelLayer',},
    "default":{"BACKEND": "channels.layers.InMemoryChannelLayer"},
}

# django-extensions configuration
SHELL_PLUS = "ipython"