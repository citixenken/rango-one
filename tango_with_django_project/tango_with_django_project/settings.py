"""
Django settings for tango_with_django_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_PATH = os.path.join(BASE_DIR,'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_igx1igy*(z@#mj8vst$yx=hwwxho(#5#ef8-e*$^6t#xl*dpo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin', #provides django with access to authentication system
    'django.contrib.auth',
    'django.contrib.contenttypes', #used by authentication application to track models installed in database
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'rango',
	'registration',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tango_with_django_project.urls'

WSGI_APPLICATION = 'tango_with_django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_PATH = os.path.join(BASE_DIR,'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
	STATIC_PATH,
)

TEMPLATE_DIRS = [
#"C:/Users/user/Desktop/django/tango_with_django_project/"
TEMPLATE_PATH,
]

#print __file__
#print os.path.dirname(__file__)
#print os.path.dirname(os.path.dirname(__file__))
#print os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PASSWORD_HASHERS = (
'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
'django.contrib.auth.hashers.BCryptPasswordHasher',
'django.contrib.auth.hashers.PBKDF2PasswordHasher',
'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

REGISTRATION_OPEN = True #if true, users can register.
ACCOUNT_ACTIVATION_DAYS = 7 #one week activation window.
REGISTRATION_AUTO_LOGIN = True #if true, user will be automatically logged in.
LOGIN_REDIRECT_URL = '/rango/' #page users arrive at after successful login.
LOGIN_URL = '/accounts/login/'

