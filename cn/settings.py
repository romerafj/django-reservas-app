import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv # Good, keep this line

load_dotenv() # Good, keep this line. It loads variables from your .env file.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SCHEDULER_AUTOSTART = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# With dotenv, this will now correctly get the SECRET_KEY from your .env locally
# and from Render's environment variables in production.
# No need for a fallback string here, as os.environ.get will return None if not set,
# which is handled by Django's startup checks.
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Reads 'DEBUG' from environment variables. 'False' is the default if not set.
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# Define ALLOWED_HOSTS
# Reads 'ALLOWED_HOSTS' from environment variables.
# In local, it comes from your .env (e.g., '127.0.0.1,localhost').
# In Render, it comes from Render's config (e.g., 'your-app.onrender.com').
# The 'if DEBUG' block for appending localhost/127.0.0.1 is now redundant
# because you're explicitly defining it in your .env. Removing it simplifies the logic.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reservas', # Make sure 'reservas' is listed only once here.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'cn' / 'templates'],
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

WSGI_APPLICATION = 'cn.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Define a base configuration for local MySQL
# This will be used if DATABASE_URL is NOT present (i.e., in local development
# unless you specifically set DATABASE_URL in your .env for local PostgreSQL testing).
LOCAL_MYSQL_DB_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'reservas_bd',
    'USER': 'app_vuelos',
    'PASSWORD': 'Aa918865512',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'OPTIONS': {'charset': 'utf8mb4'},
    'CONN_MAX_AGE': 600,
}

# The default database configuration will be local MySQL
DATABASES = {
    'default': LOCAL_MYSQL_DB_CONFIG
}

# If DATABASE_URL is present (e.g., in Render),
# then override the 'default' configuration to use PostgreSQL.
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        default=os.environ['DATABASE_URL'], # Force the use of DATABASE_URL
        conn_max_age=600,
        ssl_require=True # VERY IMPORTANT for PostgreSQL on Render
    )
    # Render uses psycopg2 (PostgreSQL), so ensure the ENGINE is correct.
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Where static files will be collected in production

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/reservas/' # Redirect user to reservations list after successful login
LOGOUT_REDIRECT_URL = '/accounts/login/' # Redirect user to login page after logout


# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com' # Brevo SMTP Server
EMAIL_PORT = 587 # Brevo SMTP Port
# IMPORTANT! Email credentials should be in environment variables for security.
# Now reads directly from environment variables (from .env locally, from Render in production).
# Removed local fallback, as it's handled by .env.
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True # TLS is recommended
DEFAULT_FROM_EMAIL = 'romerafj@gmail.com' # If this address is fixed, it can stay. Otherwise, also an environment variable.