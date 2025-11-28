import os
from pathlib import Path

from dotenv import load_dotenv

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env
load_dotenv(BASE_DIR / ".env")

# Seguridad
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "tu-clave-secreta-aqui")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() in ("1", "true", "yes")
DEBUG_PROPAGATE_EXCEPTIONS = True

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AI_CLASSIFICATION_PROMPT = os.getenv(
    "AI_CLASSIFICATION_PROMPT",
    (
        "Analizá el artículo provisto y devolvé únicamente un JSON válido con este formato: "
        '{"categorias": ["categoria 1", "categoria 2"], '
        '"resumen": "Resumen conciso en español (máximo 100 palabras).", '
        '"confianza": 0.0}. '
        "Las categorías disponibles son: {categorias}. Si no encaja exactamente, elegí la más cercana "
        "y no inventes otras nuevas. La confianza debe ser un número entre 0 y 1. Ahora analizá el siguiente contenido:\n"
    ),
)

ALLOWED_HOSTS = ["*"]

# Aplicaciones instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "import_export",
    "widget_tweaks",
    # Tu app
    "app",
    # Captcha
    "captcha",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = "Minerva.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "app.context_processors.configuracion_sistema",
            ],
        },
    },
]

WSGI_APPLICATION = "Minerva.wsgi.application"

# Base de datos
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
]

# Internacionalización
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = "/static/"


STATICFILES_DIRS = [
    BASE_DIR / "static",
]


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Campo por defecto para modelos
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Configuración de Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
