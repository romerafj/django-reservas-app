import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env si existe (para desarrollo local)
load_dotenv()

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración del scheduler (si no lo estás usando, considera eliminar esta línea)
SCHEDULER_AUTOSTART = True

# Clave secreta (OBTENIDA DE LAS VARIABLES DE ENTORNO)
# ¡IMPORTANTE!: Asegúrate de que SECRET_KEY esté configurada en las variables de entorno de Railway
# y en tu archivo .env local.
SECRET_KEY = os.environ.get('SECRET_KEY')

# Modo DEBUG (OBTENIDO DE LAS VARIABLES DE ENTORNO)
# En producción (Railway), DEBUG debe ser False. En desarrollo local, True.
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# Hosts permitidos (OBTENIDOS DE LAS VARIABLES DE ENTORNO)
# Para Railway, esto incluirá el dominio de tu aplicación. Para local, '127.0.0.1,localhost'.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')


# Definición de aplicaciones Django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reservas', # Asegúrate de que tu app 'reservas' esté listada aquí
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Para servir archivos estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs del proyecto
ROOT_URLCONF = 'cn.urls'

# Configuración de plantillas
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
                'django.template.context_processors.messages',
            ],
        },
    },
]

# Aplicación WSGI
WSGI_APPLICATION = 'cn.wsgi.application'

# Configuración de Base de Datos
# Configuración para desarrollo local con MySQL
LOCAL_DB_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'reservas_bd',
    'USER': 'app_vuelos',
    'PASSWORD': 'Aa918865512',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'OPTIONS': {'charset': 'utf8mb4'},
    'CONN_MAX_AGE': 600,
}

# Decide qué configuración de base de datos usar
# Si DATABASE_URL está presente (en Railway/producción), usa PostgreSQL.
# De lo contrario, usa la configuración local (MySQL o SQLite).
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ['DATABASE_URL'],
            conn_max_age=600,
            ssl_require=True # Mantenlo, no molesta y es bueno para la seguridad con DBs externas
        )
    }
    # Asegura que el motor sea PostgreSQL, aunque dj_database_url ya debería inferirlo
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'
else:
    # Usa la configuración de base de datos local
    DATABASES = {
        'default': LOCAL_DB_CONFIG
    }

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalización
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Archivos estáticos (CSS, JavaScript, Imágenes)
STATIC_URL = 'static/'
# Directorio donde Django recolectará todos los archivos estáticos en producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Configuración de campos de clave primaria
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URLs de redirección para autenticación
LOGIN_REDIRECT_URL = '/reservas/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Configuración de Email (Brevo/SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Credenciales de email (OBTENIDAS DE LAS VARIABLES DE ENTORNO)
# ¡IMPORTANTE!: Asegúrate de que EMAIL_HOST_USER y EMAIL_HOST_PASSWORD estén
# configuradas en las variables de entorno de Railway y en tu archivo .env local.
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'romerafj@gmail.com'