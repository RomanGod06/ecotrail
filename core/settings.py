import os
from pathlib import Path
import environ
import dj_database_url

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environ
env = environ.Env()

# SAFELY check if .env exists (it exists locally, but NOT on Render)
env_file = os.path.join(BASE_DIR, '.env')
if os.path.isfile(env_file):
    environ.Env.read_env(env_file)

# Pull the SECRET_KEY from Render's environment, fallback to a dummy key locally
SECRET_KEY = env('SECRET_KEY', default='CHANGE-ME-IN-PRODUCTION')

# DEBUG should be False on Render! We read this from the environment too.
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = ['*'] # In production, restrict this to your actual Render URL

# ... [Keep your INSTALLED_APPS and MIDDLEWARE here] ...

# DATABASE CONFIGURATION
# Set the DATABASE_URL inside your Render Dashboard Environment Variables!
# Format: postgresql://USER:PASSWORD_WITH_%40_INSTEAD_OF_@_SYMBOL@HOST:PORT/DB
DATABASES = {
    'default': dj_database_url.parse(
        'postgresql://postgres.tvmvzkqkjlkbwjpelhsy:1234@Tanu0608p@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres', # <-- Added missing comma here
        conn_max_age=0,           # Forces Django to release connections immediately
        conn_health_checks=True,  # Verifies the connection is alive before using it
    )
}

# 2. Add the Django-specific OPTIONS correctly
DATABASES['default']['OPTIONS'] = {
    'options': '-c statement_timeout=30000',
    'connect_timeout': 10, # Optional: Kills runaway queries after 30s
}

# 3. Handle Server Side Cursors
# dj_database_url handles this slightly differently than raw Django dicts.
# We set it at the root of the default db config, not inside the psycopg2 OPTIONS.
DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'rest_framework',
    'corsheaders',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


LOGIN_REDIRECT_URL = '/api/add-hotel/'  # Where to go after logging in
LOGOUT_REDIRECT_URL = '/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

import os # Make sure this is imported at the top of your file!

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# This is the folder where Django will gather all your static files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Optional but highly recommended: Tells Whitenoise to compress your files so they load faster
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


CORS_ALLOW_ALL_ORIGINS = True