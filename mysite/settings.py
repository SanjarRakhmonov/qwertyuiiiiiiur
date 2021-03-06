"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#xvv1ew-aszbg%*ycpoix((@%ug&#uh*#%*4nj7nm(e8ghn+=n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.102', '127.0.0.1', '192.168.1.103', '192.168.43.209', 'libercen.herokuapp.com']
PROJECT_DIR = Path(__file__).parent

# Application definition

INSTALLED_APPS = [
    'search',
    'haystack',
    'ajaxuploader',
    'django.contrib.humanize',
    'core',
    'posts',
    'memcache_status',
    'embed_video',
    'courses',
    'actions',
	'social.apps.django_app.default',
    'sorl.thumbnail',
    'images',
    'user',
    'taggit',
    'filebrowser',
    'ajax_select',  
    'easy_thumbnails',
	'django.contrib.sites',
	'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
]
SITE_ID=3


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
			'debug': DEBUG,
            'context_processors': [
				'django.template.context_processors.i18n',
				'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
				
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

AUTHENTICATION_BACKENDS = (
'django.contrib.auth.backends.ModelBackend',
'user.authentication.EmailAuthBackend',
'social.backends.facebook.Facebook2OAuth2',
'social.backends.twitter.TwitterOAuth',
)


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = PROJECT_DIR.parent.child('staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = 'knowldg.for.everyone@gmail.com'
EMAIL_HOST_PASSWORD = 'knowldgokey123'
SOCIALACCOUNT_QUERY_EMAIL = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
"""
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
"""
HAYSTACK_CONNECTIONS = {
	'default': {
		'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
		'URL': 'http://127.0.0.1:8983/solr/user'
	},
}


ANONYMOUS_USER_ID = -1

POSTMAN_DISALLOW_ANONYMOUS=True
POSTMAN_DISABLE_USER_EMAILING=True
POSTMAN_AUTOCOMPLETER_APP='ajax_select'

GRAPPELLI_ADMIN_TITLE = "Knowldg.com"
GRAPPELLI_CLEAN_INPUT_TYPES = True
from django.core.urlresolvers import reverse_lazy
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')


SOCIAL_AUTH_FACEBOOK_KEY = '914603965333386' # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'd434b6dc444ba1f41d6d9c86be1bcddc' # Facebook App Secret

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']


SOCIAL_AUTH_TWITTER_KEY = 'h1NKoagd7U7WmncIgcNYPFoGb' # Twitter Consumer Key
SOCIAL_AUTH_TWITTER_SECRET = 'VBXXrdnxy3nQmRpG7KRYubU4ESzGWitLkZHW1RUZyXhcG8Fwwg' # Twitter Consumer Secret

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '786373494704-104nfd2gcnpt0k9rf99d1fbhvg4375kg.apps.googleusercontent.com' # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'bjuUa2bH32eDmFIbEKZZkTJe' # Google Consumer Secret



ABSOLUTE_URL_OVERRIDES = {
'auth.user': lambda u: reverse_lazy('user_detail',
args=[u.username])
}


TAGGIT_CASE_INSENSITIVE = True



CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

###############################
#       SOLR  SETTINGS       #
##############################
SOLR_CONN = 'http://SOLRSERVER:8983/solr'
