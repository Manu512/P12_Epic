"""
Django settings for EPIC_Event project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b%kva5s*iep7z#3$ebl4ntu1x!)anzh6&h6%%iw!7mu^)ht1#w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

]

THIRD_PARTY_APPS = [
        'django_filters',
        'debug_toolbar',
        'django_extensions',
        'rest_framework',
        'phonenumber_field',
]

PROJECT_APPS = [
        'user.apps.UserConfig',
        'api.apps.ApiConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'EPIC_Event.urls'

TEMPLATES = [
        {
                'BACKEND':  'django.template.backends.django.DjangoTemplates',
                'DIRS':     [BASE_DIR / 'templates'],
                'APP_DIRS': True,
                'OPTIONS':  {
                        'context_processors': [
                                'django.template.context_processors.debug',
                                'django.template.context_processors.request',
                                'django.contrib.auth.context_processors.auth',
                                'django.contrib.messages.context_processors.messages',
                        ],
                },
        },
]

WSGI_APPLICATION = 'EPIC_Event.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {

        'default': {
                'ENGINE':   'django.db.backends.postgresql_psycopg2',
                'NAME':     'epic_event',
                'USER':     'epic',
                'PASSWORD': '4625',
                'HOST':     '192.168.1.8',
                'PORT':     '5432',
        }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

DATETIME_FORMAT = '%d/%m/%Y %H:%M'
DATE_FORMAT = '%d/%m/%Y'
TIME_FORMAT = '%H:%M'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
        '127.0.0.1',
]

AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS':       'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE':                      10,
        'DEFAULT_PERMISSION_CLASSES':     (
                'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_RENDERER_CLASSES':       (
                'rest_framework.renderers.JSONRenderer',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework.authentication.SessionAuthentication',
                'rest_framework.authentication.BasicAuthentication',
                'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_FILTER_BACKENDS':        ('django_filters.rest_framework.DjangoFilterBackend',),
}

SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME':           timedelta(hours=1),
        'REFRESH_TOKEN_LIFETIME':          timedelta(days=1),
        'ROTATE_REFRESH_TOKENS':           False,
        'BLACKLIST_AFTER_ROTATION':        True,
        'UPDATE_LAST_LOGIN':               False,

        'ALGORITHM':                       'HS256',
        'SIGNING_KEY':                     SECRET_KEY,
        'VERIFYING_KEY':                   None,
        'AUDIENCE':                        None,
        'ISSUER':                          None,

        'AUTH_HEADER_TYPES':               ('Bearer',),
        'AUTH_HEADER_NAME':                'HTTP_AUTHORIZATION',
        'USER_ID_FIELD':                   'id',
        'USER_ID_CLAIM':                   'user_id',

        'AUTH_TOKEN_CLASSES':              ('rest_framework_simplejwt.tokens.AccessToken',),
        'TOKEN_TYPE_CLAIM':                'token_type',

        'JTI_CLAIM':                       'jti',

}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'file',
        },
        'console': {
                'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
                'handlers': ['file', 'console'],
                'level': 'ERROR',
                'propagate': True,
                'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR')
        },
    },
}
