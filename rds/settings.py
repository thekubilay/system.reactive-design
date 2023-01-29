import os

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ["localhost", "system.reactive-design.com"]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = []

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.sites',
]

INSTALLED_APPS += [
  "settings",
  "teams",
  "projects",
  "tasks",

  'rest_framework',
  'rest_framework.authtoken', 'allauth',
  'allauth.account',
  'allauth.socialaccount',
  'allauth.socialaccount.providers.asana',
  'rest_auth',
  'rest_auth.registration', 'corsheaders',
  'crispy_forms',
  'webpack_loader',
  'django_crontab',
  'dbbackup',

]

SITE_ID = 1

LOGIN_URL = "accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
  'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rds.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
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

WEBPACK_LOADER = {
  "DEFAULT": {
    "BUNDLE_DIR_NAME": "dist/",
    "STATS_FILE": os.path.join(BASE_DIR, "vue", "webpack-stats.json")
  }
}

WSGI_APPLICATION = 'rds.wsgi.application'

if DEBUG:
  DATABASES = {
    'default': {
      'ENGINE': 'mysql.connector.django',
      'NAME': 'rds',
      'USER': 'root',
      'PASSWORD': 'snickers.007',
      'HOST': 'localhost',
      'PORT': '3306'
    }
  }
else:
  DATABASES = {
    'default': {
      'ENGINE': 'mysql.connector.django',
      'NAME': 'reactive-design-system',
      'USER': 'root',
      'PASSWORD': 'SnckrXYsnXpG1_',
      'HOST': 'localhost',
      'PORT': '3306'
    }
  }
#
# DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
# DBBACKUP_STORAGE_OPTIONS = {'location': '/backup/'}
# CUSTOM_CONNECTOR_MAPPING = {
#   "mysql.connector.django": "dbbackup.db.mysql.MysqlDumpConnector"
# }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CRONJOB
CRONJOBS = [
  ('*/10 * * * *', 'projects.cron.crawl_asana'),
]

# SMTP CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)

if DEBUG:
  STATIC_URL = '/static/'
  STATICFILES_DIRS = [
    BASE_DIR / "static",
    'static',
  ]
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  MEDIA_URL = '/media/'
else:
  MEDIA_URL = '/media/'
  STATIC_URL = '/static/'
  STATICFILES_DIRS = [
    'rds/static',
  ]
