"""
Configurações do Django para o projeto Gestão ERP.

Este arquivo contém todas as configurações do projeto, incluindo:
- Configurações de segurança
- Aplicativos instalados
- Middleware
- Banco de dados
- Internacionalização
- Arquivos estáticos

Gerado por 'django-admin startproject' usando Django 5.2.9.

Para mais informações sobre este arquivo, consulte:
https://docs.djangoproject.com/en/5.2/topics/settings/

Para a lista completa de configurações e seus valores, consulte:
https://docs.djangoproject.com/en/5.2/ref/settings/

Autor: Manus AI
Data: 2025-12-02
"""

from pathlib import Path

# =============================================================================
# CAMINHOS DO PROJETO
# =============================================================================

# Diretório base do projeto: /caminho/para/gestao_erp/
BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA
# =============================================================================

# ATENÇÃO: Mantenha a chave secreta em produção!
# Em produção, use variáveis de ambiente para armazenar a SECRET_KEY
SECRET_KEY = 'django-insecure-r_e%n-0@n8fit$xx3c+p-%g(%p$36+#@zr%7%p#+jx0j#abta%'

# ATENÇÃO: Nunca execute com DEBUG=True em produção!
# Em produção, defina DEBUG=False
DEBUG = True

# Hosts permitidos para acessar a aplicação
# Em produção, especifique os domínios permitidos, ex: ['meusite.com', 'www.meusite.com']
ALLOWED_HOSTS = []


# =============================================================================
# APLICAÇÕES INSTALADAS
# =============================================================================

INSTALLED_APPS = [
    # Aplicações padrão do Django
    'django.contrib.admin',          # Painel de administração
    'django.contrib.auth',           # Sistema de autenticação
    'django.contrib.contenttypes',   # Framework de tipos de conteúdo
    'django.contrib.sessions',       # Framework de sessões
    'django.contrib.messages',       # Framework de mensagens
    'django.contrib.staticfiles',    # Gerenciamento de arquivos estáticos
    
    # Aplicações do projeto
    'estoque',      # Módulo de controle de estoque
    'financeiro',   # Módulo de controle financeiro
]


# =============================================================================
# MIDDLEWARE
# =============================================================================

# Middleware são componentes que processam requisições/respostas
# A ordem é importante!
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',           # Segurança
    'django.contrib.sessions.middleware.SessionMiddleware',    # Sessões
    'django.middleware.common.CommonMiddleware',               # Funcionalidades comuns
    'django.middleware.csrf.CsrfViewMiddleware',              # Proteção CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Autenticação
    'django.contrib.messages.middleware.MessageMiddleware',    # Mensagens
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Proteção clickjacking
]


# =============================================================================
# CONFIGURAÇÕES DE URL E WSGI
# =============================================================================

# Arquivo principal de configuração de URLs
ROOT_URLCONF = 'gestao_erp.urls'

# Aplicação WSGI para deploy em produção
WSGI_APPLICATION = 'gestao_erp.wsgi.application'


# =============================================================================
# CONFIGURAÇÕES DE TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        # Diretórios onde o Django procura por templates
        'DIRS': [BASE_DIR / 'templates'],
        
        # Permite que cada app tenha seu próprio diretório de templates
        'APP_DIRS': True,
        
        # Processadores de contexto (variáveis disponíveis em todos os templates)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',      # Variáveis de debug
                'django.template.context_processors.request',    # Objeto request
                'django.contrib.auth.context_processors.auth',   # Usuário autenticado
                'django.contrib.messages.context_processors.messages',  # Mensagens
            ],
        },
    },
]


# =============================================================================
# CONFIGURAÇÕES DE BANCO DE DADOS
# =============================================================================

# Por padrão, usa SQLite (ideal para desenvolvimento)
# Em produção, considere usar PostgreSQL ou MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Exemplo de configuração para PostgreSQL (comentado):
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'gestao_erp',
#         'USER': 'seu_usuario',
#         'PASSWORD': 'sua_senha',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# =============================================================================
# VALIDAÇÃO DE SENHAS
# =============================================================================

# Validadores que garantem senhas seguras
AUTH_PASSWORD_VALIDATORS = [
    {
        # Verifica similaridade com atributos do usuário
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Exige comprimento mínimo de 8 caracteres
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Verifica se a senha não é muito comum
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Verifica se a senha não é totalmente numérica
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =============================================================================
# INTERNACIONALIZAÇÃO
# =============================================================================

# Idioma padrão da aplicação
LANGUAGE_CODE = 'pt-br'  # Português do Brasil

# Fuso horário
TIME_ZONE = 'America/Sao_Paulo'  # Horário de Brasília

# Habilita internacionalização (i18n)
USE_I18N = True

# Usa timezone-aware datetimes
USE_TZ = True


# =============================================================================
# ARQUIVOS ESTÁTICOS (CSS, JavaScript, Imagens)
# =============================================================================

# URL para acessar arquivos estáticos
STATIC_URL = 'static/'

# Diretório onde os arquivos estáticos serão coletados em produção
# Execute 'python manage.py collectstatic' antes do deploy
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Diretórios adicionais para arquivos estáticos
STATICFILES_DIRS = [
    # BASE_DIR / 'static',
]


# =============================================================================
# ARQUIVOS DE MÍDIA (Uploads de usuários)
# =============================================================================

# URL para acessar arquivos de mídia
MEDIA_URL = 'media/'

# Diretório onde os arquivos de mídia serão armazenados
MEDIA_ROOT = BASE_DIR / 'media'


# =============================================================================
# CONFIGURAÇÕES DE AUTENTICAÇÃO
# =============================================================================

# URL de redirecionamento após login
LOGIN_REDIRECT_URL = '/'

# URL de redirecionamento após logout
LOGOUT_REDIRECT_URL = '/login/'

# URL da página de login
LOGIN_URL = '/login/'


# =============================================================================
# CONFIGURAÇÕES GERAIS
# =============================================================================

# Tipo de campo de chave primária padrão
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA PARA PRODUÇÃO
# =============================================================================

# Descomente as linhas abaixo ao fazer deploy em produção:

# Força o uso de HTTPS
# SECURE_SSL_REDIRECT = True

# Cookies de sessão apenas via HTTPS
# SESSION_COOKIE_SECURE = True

# Cookies CSRF apenas via HTTPS
# CSRF_COOKIE_SECURE = True

# Previne que o navegador detecte o content-type
# SECURE_CONTENT_TYPE_NOSNIFF = True

# Proteção XSS no navegador
# SECURE_BROWSER_XSS_FILTER = True

# Força HTTPS por 1 ano
# SECURE_HSTS_SECONDS = 31536000

# Inclui subdomínios no HSTS
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Pré-carrega HSTS
# SECURE_HSTS_PRELOAD = True

# Proteção contra clickjacking
# X_FRAME_OPTIONS = 'DENY'


# =============================================================================
# CONFIGURAÇÕES DE EMAIL (para notificações)
# =============================================================================

# Exemplo de configuração de email (comentado):
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'seu_email@gmail.com'
# EMAIL_HOST_PASSWORD = 'sua_senha_de_app'
# DEFAULT_FROM_EMAIL = 'seu_email@gmail.com'


# =============================================================================
# CONFIGURAÇÕES DE LOGGING (para debug e monitoramento)
# =============================================================================

# Configuração básica de logging
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

# Criar diretório de logs se não existir
import os
os.makedirs(BASE_DIR / 'logs', exist_ok=True)
