"""
Django settings for chihu project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'loqqa8avv%ibpe*0&t^(=w^jutu39^gf$gv$^tbt3nug@vhvu2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chihuapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'chihu.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'chihu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

#from sae
SAE_MYSQL_HOST = 'w.rdc.sae.sina.com.cn'
SAE_MYSQL_PORT = '3307'
SAE_MYSQL_USER = '3ww0j1o0lz'
SAE_MYSQL_PASS = '203x20hi2lwikki1mjwmzx32ijwkhj4l0y45jiy1'
SAE_MYSQL_DB   = 'app_chihusysu'

#local db setting
LOCAL_MYSQL_DB = 'chihu'
LOCAL_MYSQL_USER = 'chen'
LOCAL_MYSQL_PASS = 'chen'
LOCAL_MYSQL_HOST = 'localhost'
LOCAL_MYSQL_PORT = '3306'


if not DEBUG:
    DATABASES = {
        'default': {   
            'ENGINE': 'django.db.backends.mysql',
            'NAME': SAE_MYSQL_DB,
            'USER': SAE_MYSQL_USER,
            'PASSWORD': SAE_MYSQL_PASS,
            'HOST': SAE_MYSQL_HOST,
            'PORT': SAE_MYSQL_PORT,
        }
    }    
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': LOCAL_MYSQL_DB,
            'USER': LOCAL_MYSQL_USER,
            'PASSWORD': LOCAL_MYSQL_PASS,
            'HOST': LOCAL_MYSQL_HOST,
            'PORT': LOCAL_MYSQL_PORT,
        }
    }
        


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
