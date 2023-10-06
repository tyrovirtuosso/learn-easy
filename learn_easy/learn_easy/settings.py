from pathlib import Path
from dotenv import load_dotenv
import os
import logging
from celery.schedules import crontab


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
    "cards.apps.CardsConfig",
    "decks.apps.DecksConfig",
    "dashboard.apps.DashboardConfig",
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
    # Celery Beat for cronjobs
    "django_celery_beat",
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
LOGIN_REDIRECT_URL = "dashboard"
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

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# Connecting to Custom Serverless Cloud PostgreSQL DB
HOST=os.environ.get('AWS_POSTGRE_HOST')
USER=os.environ.get('AWS_POSTGRE_USERNAME')
PASSWORD=os.environ.get('AWS_POSTGRE_PASSWORD')
PORT=int(os.environ.get('AWS_POSTGRE_PORT'))
DATABASE=os.environ.get('AWS_POSTGRE_DATABASE')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
    }}


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

LOGOUT_REDIRECT_URL = "home"


# CHANNEL_LAYERS = {
#     "default":{"BACKEND": "channels.layers.InMemoryChannelLayer"},
# }

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379, 1)],  # Use database 1
        },
    },
}

# django-extensions configuration
SHELL_PLUS = "ipython"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_warnings.log'),
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'WARNING',
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


CELERY_BEAT_SCHEDULE = {
    "check_and_update_empty_cards": {
        "task": "cards.tasks.check_and_update_empty_cards",
        "schedule": crontab(minute="*/1"),
    },
}