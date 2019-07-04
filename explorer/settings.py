"""
Django settings for explorer project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import simplejson as json

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

INTERNAL_IPS = os.getenv('DEBUG_TOOLBAR_INTERNAL_IPS')

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

AUTH_USER_MODEL = 'cabinet.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'corsheaders',
    'rest_framework',
    'api',
    'cabinet',
    'scan',
    'java_wallet',
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

ROOT_URLCONF = 'explorer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'scan.context_processors.settings_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'explorer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_DEFAULT_ENGINE'),
        'NAME': os.getenv('DB_DEFAULT_NAME'),
        'HOST': os.getenv('DB_DEFAULT_HOST'),
        'USER': os.getenv('DB_DEFAULT_USER'),
        'PASSWORD': os.getenv('DB_DEFAULT_PASSWORD'),
        'OPTIONS': json.loads(os.getenv('DB_DEFAULT_OPTIONS')),
    },
    'java_wallet': {
        'ENGINE': os.getenv('DB_JAVA_WALLET_ENGINE'),
        'NAME': os.getenv('DB_JAVA_WALLET_NAME'),
        'HOST': os.getenv('DB_JAVA_WALLET_HOST'),
        'USER': os.getenv('DB_JAVA_WALLET_USER'),
        'PASSWORD': os.getenv('DB_JAVA_WALLET_PASSWORD'),
        'OPTIONS': json.loads(os.getenv('DB_JAVA_WALLET_OPTIONS')),
    },
}

DATABASE_ROUTERS = ['java_wallet.db_router.DBRouter', 'scan.db_router.DBRouter']


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CACHES = {
    'default': {
        'BACKEND': os.getenv('CACHE_BACKEND'),
        'LOCATION': os.getenv('CACHE_LOCATION'),
        'TIMEOUT': os.getenv('CACHE_TIMEOUT'),
        'OPTIONS': json.loads(os.getenv('CACHE_OPTIONS')),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'scan': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

ACCOUNTS_NAME_FORCE = [
    3011184961392690771,
    1606939141091290673,
    3463450404564580757,
    6368006909961888739,
]

SENTRY_DSN = os.getenv('SENTRY_DSN')

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration()]
    )

# UA-XXXXXXXXX-X
GOOGLE_TRACKING_ID = os.getenv('GOOGLE_TRACKING_ID')

BRS_NODE = os.getenv('BRS_NODE')

WALLET_URL = os.getenv('WALLET_URL')

BRS_BOOTSTRAP_PEERS = [
    'wallet.burst.devtrue.net:443',
    'wallet.burstcoin.network:8125',
]

# for fork solving
AGGR_STORE_BLOCK_SIGNATURE = 3600 * 24 * 7

TEST_NET = os.getenv('TEST_NET')
