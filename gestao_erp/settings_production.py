"""
Configuracoes de Producao para o Django ERP.

Este arquivo estende as configuracoes base e adiciona parametros
especificos para ambiente de producao.

Uso:
    export DJANGO_SETTINGS_MODULE=gestao_erp.settings_production
    python manage.py runserver
"""

from .settings import *
import os
from decouple import config

# =============================================================================
# CONFIGURACOES DE SEGURANCA PARA PRODUCAO
# =============================================================================

# Desabilitar modo debug em producao
DEBUG = False

# Redirecionar HTTP para HTTPS
SECURE_SSL_REDIRECT = True

# Proteger cookies de sessao
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Impedir ataques de MIME sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Proteger contra ataques XSS
SECURE_BROWSER_XSS_FILTER = True

# Habilitar HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Politica de referrer
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# =============================================================================
# CONFIGURACAO DE BANCO DE DADOS PARA PRODUCAO
# =============================================================================

# Usar PostgreSQL em producao
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='gestao_erp'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'ATOMIC_REQUESTS': True,  # Usar transacoes atomicas para integridade
        'CONN_MAX_AGE': 600,  # Manter conexoes por 10 minutos
    }
}

# =============================================================================
# CONFIGURACAO DE CACHE
# =============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# =============================================================================
# CONFIGURACAO DE EMAIL
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@gestaoerp.com.br')

# =============================================================================
# CONFIGURACAO DE LOGGING PARA PRODUCAO
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'security.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'audit_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'audit.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'auditoria': {
            'handlers': ['audit_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Criar diretorio de logs se nao existir
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# =============================================================================
# CONFIGURACAO DE SESSAO
# =============================================================================

# Tempo de sessao (em segundos) - 24 horas
SESSION_COOKIE_AGE = 86400

# Expirar sessao ao fechar navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Salvar sessao em cada requisicao
SESSION_SAVE_EVERY_REQUEST = False

# =============================================================================
# CONFIGURACAO DE ALLOWED HOSTS
# =============================================================================

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# =============================================================================
# CONFIGURACAO DE ARQUIVOS ESTATICOS
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
