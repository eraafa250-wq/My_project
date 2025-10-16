from pathlib import Path
import os
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Основные настройки ---
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = ["mededu.com.kz", "www.mededu.com.kz", "mededu-74f7.onrender.com"]

# --- Приложения ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # ВАЖНО: cloudinary должны быть ДО ckeditor и users
    'cloudinary_storage',
    'cloudinary',
    
    'ckeditor',
    'ckeditor_uploader',
    'users',
]

# --- Middleware ---
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

ROOT_URLCONF = 'EDU.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'EDU.wsgi.application'

# --- База данных ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# --- Пароли ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Локализация ---
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Cloudinary настройки для медиафайлов ---
import cloudinary

# Cloudinary автоматически читает CLOUDINARY_URL из переменных окружения
cloudinary.config(
    cloud_name = config('CLOUDINARY_CLOUD_NAME', default='dnhrazwau'),
    api_key = config('CLOUDINARY_API_KEY', default='816967332389659'),
    api_secret = config('CLOUDINARY_API_SECRET', default='519gtXPAAKas6u6v5kbpKyvMEeg')
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default='dnhrazwau'),
    'API_KEY': config('CLOUDINARY_API_KEY', default='816967332389659'),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default='519gtXPAAKas6u6v5kbpKyvMEeg')
}

# Используем Cloudinary для всех медиафайлов (ImageField)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --- Статика ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- CKEditor ---
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
# Удалена строка CKEDITOR_STORAGE_BACKEND - она не поддерживается
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraAllowedContent': 'iframe[*]',
        'height': 300,
        'width': '100%',
    }
}

# Медиа URL (для совместимости с CKEditor)
MEDIA_URL = '/media/'

# --- Редиректы ---
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'