"""
Configurações do Django para o projeto Gestão ERP.

Este arquivo foi refatorado para usar variáveis de ambiente (python-decouple)
e suportar configurações seguras para produção.

Autor: Denis Barbosa (Todos os direitos reservados)
Data da Refatoração: 2026-02-17
"""

import os
from pathlib import Path
import dj_database_url
from decouple import config, Csv

# =============================================================================
# CAMINHOS DO PROJETO
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA (Via Variáveis de Ambiente)
# =============================================================================

# Nunca execute com DEBUG=True em produção!
DEBUG = config('DEBUG', default=False, cast=bool)

# Chave secreta carregada do .env (Nunca suba para o GitHub!)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-mudar-em-producao')

# Hosts permitidos
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())


# =============================================================================
# APLICAÇÕES INSTALADAS
# =============================================================================

INSTALLED_APPS = [
    # Aplicações padrão do Django
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Aplicações do projeto
    'estoque',
    'financeiro',
    'fiscal',
    'fornecedores',
    'clientes',
    'pdv',
    'auditoria',
    'vendas',
    'relatorios',
    'notificacoes',
    'companies',
    'base',
    
    # Bibliotecas de terceiros
    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_spectacular',
]


# =============================================================================
# MIDDLEWARE
# =============================================================================

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
    'companies.middleware.TenantMiddleware',
]


# =============================================================================
# CONFIGURAÇÕES DE URL E WSGI
# =============================================================================

ROOT_URLCONF = 'gestao_erp.urls'
WSGI_APPLICATION = 'gestao_erp.wsgi.application'


# =============================================================================
# CONFIGURAÇÕES DE TEMPLATES
# =============================================================================

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


# =============================================================================
# CONFIGURAÇÕES DE BANCO DE DADOS (Suporte a Múltiplos Motores)
# =============================================================================

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}


# =============================================================================
# VALIDAÇÃO DE SENHAS
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =============================================================================
# INTERNACIONALIZAÇÃO
# =============================================================================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# =============================================================================
# ARQUIVOS ESTÁTICOS E MÍDIA
# =============================================================================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =============================================================================
# CONFIGURAÇÕES DE AUTENTICAÇÃO
# =============================================================================

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA PARA PRODUÇÃO (Via Variáveis de Ambiente)
# =============================================================================

# Redirecionamento HTTPS e Cookies Seguros
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int) # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Outras Proteções
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# =============================================================================
# CONFIGURAÇÕES DA API (Django Rest Framework & JWT)
# =============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Gestão ERP API',
    'DESCRIPTION': 'API para o sistema de gestão de estoque e financeira',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# =============================================================================
# CONFIGURAÇÕES DE CORS
# =============================================================================

CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000,http://localhost:5173', cast=Csv())
CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# LOGGING
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# Configuração para permitir o domínio exposto pelo Manus
CSRF_TRUSTED_ORIGINS = ['https://8000-icfr5lxj5zpx7rniy8g0h-7b384c41.us1.manus.computer']
