"""
Django settings for bookstore_project project.

Generated for agile e-commerce development.
"""

from pathlib import Path
from decouple import config, Csv
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-development-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    # Add third-party apps here as needed
]

LOCAL_APPS = [
    # Add custom apps here as we develop them
    'books',
    'accounts',
    'cart',
    'orders',
    # 'reviews',
]

# Sitemap configuration
DJANGO_APPS += ['django.contrib.sitemaps']
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

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

ROOT_URLCONF = 'bookstore_project.urls'

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
                'cart.context_processors.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookstore_project.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Alternative explicit configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME', default=''),
#         'USER': config('DB_USER', default=''),
#         'PASSWORD': config('DB_PASSWORD', default=''),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Site ID for django.contrib.sites
SITE_ID = 1

# Google Books API Configuration
GOOGLE_BOOKS_API_KEY = config('GOOGLE_BOOKS_API_KEY', default='')
GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'

# Stripe Configuration (for future payment integration)
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')

# Security settings (for production)
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Login/Logout URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Sitemap configuration
SITE_ID = 1

# Add to INSTALLED_APPS if not already there
if 'django.contrib.sitemaps' not in INSTALLED_APPS:
    INSTALLED_APPS += ['django.contrib.sitemaps']

# =============================================================================
# PRODUCTION STATIC FILES (WHITENOISE)
# =============================================================================

# Whitenoise static files serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Additional whitenoise settings
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# For development testing - uncomment to print emails to console instead
# 

# When Gmail is fixed, uncomment these and comment console backend:
# 
# 
# 
# 
# 
# 

# Switch to Gmail later when ready:
# 
# 
# 
# 
# 
# 


# ===================================
# Email Configuration (Uses Environment Variables)
# ===================================
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@talesandtails.com')
SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'noreply@talesandtails.com')

# Email settings for Tales & Tails
EMAIL_SUBJECT_PREFIX = '[Tales & Tails] '
ADMINS = [('Admin', os.getenv('ADMIN_EMAIL', 'admin@talesandtails.com'))]
MANAGERS = ADMINS

# =================================
# STRIPE CONFIGURATION
# =================================
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_ENDPOINT_SECRET = config('STRIPE_ENDPOINT_SECRET', default='')

# Validate Stripe keys are loaded
if not STRIPE_PUBLISHABLE_KEY or not STRIPE_SECRET_KEY:
    print("⚠️  WARNING: Stripe keys not found in environment variables")
    print(f"STRIPE_PUBLISHABLE_KEY: {'✅' if STRIPE_PUBLISHABLE_KEY else '❌'}")
    print(f"STRIPE_SECRET_KEY: {'✅' if STRIPE_SECRET_KEY else '❌'}")
else:
    print("✅ Stripe keys loaded successfully")
