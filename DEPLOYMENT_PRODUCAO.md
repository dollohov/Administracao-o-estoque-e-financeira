# Guia de Deployment para Producao

Este documento descreve como fazer o deploy do ERP em um ambiente de producao seguro e escalavel.

---

## 1. Preparacao do Servidor

### 1.1 Requisitos Minimos

- **SO**: Ubuntu 20.04 LTS ou superior
- **Python**: 3.9+
- **PostgreSQL**: 12+
- **Redis**: 6+ (para cache)
- **Nginx**: 1.18+ (como reverse proxy)
- **Gunicorn**: Para servir a aplicacao Django

### 1.2 Instalacao de Dependencias

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib redis-server nginx git

# Instalar Gunicorn
pip3 install gunicorn
```

---

## 2. Configuracao do Banco de Dados

### 2.1 Criar Banco de Dados PostgreSQL

```bash
# Conectar ao PostgreSQL
sudo -u postgres psql

# Criar banco de dados
CREATE DATABASE gestao_erp;

# Criar usuario
CREATE USER erp_user WITH PASSWORD 'senha-segura-aqui';

# Dar permissoes
ALTER ROLE erp_user SET client_encoding TO 'utf8';
ALTER ROLE erp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE erp_user SET default_transaction_deferrable TO on;
ALTER ROLE erp_user SET default_transaction_read_committed TO on;
GRANT ALL PRIVILEGES ON DATABASE gestao_erp TO erp_user;

# Sair
\q
```

---

## 3. Configuracao da Aplicacao

### 3.1 Clonar Repositorio

```bash
# Criar diretorio
mkdir -p /var/www
cd /var/www

# Clonar repositorio
git clone https://github.com/seu-usuario/Administracao-o-estoque-e-financeira.git gestao_erp
cd gestao_erp
```

### 3.2 Criar Ambiente Virtual

```bash
# Criar venv
python3 -m venv venv

# Ativar venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3.3 Configurar Variaveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com as configuracoes de producao
nano .env
```

**Exemplo de .env para producao:**

```
DEBUG=False
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
ALLOWED_HOSTS=seu-dominio.com.br,www.seu-dominio.com.br

DB_ENGINE=django.db.backends.postgresql
DB_NAME=gestao_erp
DB_USER=erp_user
DB_PASSWORD=senha-segura-aqui
DB_HOST=localhost
DB_PORT=5432

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

REDIS_URL=redis://localhost:6379/1

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app
```

### 3.4 Executar Migracoes

```bash
# Ativar venv
source venv/bin/activate

# Executar migracoes
python manage.py migrate --settings=gestao_erp.settings_production

# Coletar arquivos estaticos
python manage.py collectstatic --noinput --settings=gestao_erp.settings_production

# Criar superusuario
python manage.py createsuperuser --settings=gestao_erp.settings_production
```

---

## 4. Configuracao do Gunicorn

### 4.1 Criar Arquivo de Configuracao

```bash
# Criar arquivo gunicorn_config.py
cat > /var/www/gestao_erp/gunicorn_config.py << 'EOF'
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
daemon = False
pidfile = "/var/run/gunicorn.pid"
umask = 0
user = "www-data"
group = "www-data"
tmp_upload_dir = None
secure_scheme_headers = {
    'FORWARDED': 'proto',
    'X-FORWARDED-PROTOCOL': 'proto',
    'X-FORWARDED-PROTO': 'proto',
    'X-FORWARDED-SSL': 'on',
    'X-FORWARDED-SCHEME': 'https',
}
forwarded_allow_ips = "*"
EOF
```

### 4.2 Criar Servico Systemd

```bash
# Criar arquivo de servico
sudo nano /etc/systemd/system/gunicorn.service
```

**Conteudo do arquivo:**

```ini
[Unit]
Description=Gunicorn application server for Gestao ERP
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/gestao_erp
Environment="PATH=/var/www/gestao_erp/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=gestao_erp.settings_production"
ExecStart=/var/www/gestao_erp/venv/bin/gunicorn \
    --config /var/www/gestao_erp/gunicorn_config.py \
    gestao_erp.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
KillSignal=SIGQUIT
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### 4.3 Iniciar Servico

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar servico
sudo systemctl enable gunicorn

# Iniciar servico
sudo systemctl start gunicorn

# Verificar status
sudo systemctl status gunicorn
```

---

## 5. Configuracao do Nginx

### 5.1 Criar Arquivo de Configuracao

```bash
# Criar arquivo de configuracao
sudo nano /etc/nginx/sites-available/gestao_erp
```

**Conteudo do arquivo:**

```nginx
upstream gunicorn {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name seu-dominio.com.br www.seu-dominio.com.br;
    
    # Redirecionar HTTP para HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seu-dominio.com.br www.seu-dominio.com.br;
    
    # Certificados SSL (usar Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/seu-dominio.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com.br/privkey.pem;
    
    # Configuracoes SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Seguranca
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    client_max_body_size 100M;
    
    location /static/ {
        alias /var/www/gestao_erp/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /var/www/gestao_erp/media/;
        expires 7d;
    }
    
    location / {
        proxy_pass http://gunicorn;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### 5.2 Habilitar Site

```bash
# Criar link simbolico
sudo ln -s /etc/nginx/sites-available/gestao_erp /etc/nginx/sites-enabled/

# Testar configuracao
sudo nginx -t

# Recarregar Nginx
sudo systemctl reload nginx
```

---

## 6. Certificado SSL (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obter certificado
sudo certbot certonly --nginx -d seu-dominio.com.br -d www.seu-dominio.com.br

# Renovacao automatica (ja configurada)
sudo systemctl enable certbot.timer
```

---

## 7. Backup e Recuperacao

### 7.1 Script de Backup

```bash
# Criar script de backup
cat > /usr/local/bin/backup_erp.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/backups/erp"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="gestao_erp"
DB_USER="erp_user"

# Criar diretorio se nao existir
mkdir -p $BACKUP_DIR

# Backup do banco de dados
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup de arquivos
tar -czf $BACKUP_DIR/files_$DATE.tar.gz /var/www/gestao_erp/media/

# Remover backups antigos (manter ultimos 30 dias)
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup concluido: $DATE"
EOF

# Dar permissao de execucao
chmod +x /usr/local/bin/backup_erp.sh

# Agendar backup diario (adicionar ao crontab)
# 0 2 * * * /usr/local/bin/backup_erp.sh
```

---

## 8. Monitoramento

### 8.1 Verificar Logs

```bash
# Logs do Gunicorn
sudo journalctl -u gunicorn -f

# Logs do Nginx
sudo tail -f /var/log/nginx/error.log

# Logs da Aplicacao
tail -f /var/www/gestao_erp/logs/django.log
```

### 8.2 Monitorar Recursos

```bash
# Instalar ferramentas de monitoramento
sudo apt install -y htop iotop nethogs

# Monitorar em tempo real
htop
```

---

## 9. Checklist de Seguranca

- [ ] DEBUG=False em producao
- [ ] SECRET_KEY alterada e segura
- [ ] ALLOWED_HOSTS configurado corretamente
- [ ] SSL/HTTPS ativado
- [ ] Backup automatizado configurado
- [ ] Logs de auditoria habilitados
- [ ] Firewall configurado (ufw)
- [ ] Atualizacoes de seguranca aplicadas
- [ ] Senhas fortes para banco de dados
- [ ] Permissoes de arquivo corretas (755 para diretorios, 644 para arquivos)

---

## 10. Troubleshooting

### Erro: "Permission denied" ao acessar arquivos

```bash
# Corrigir permissoes
sudo chown -R www-data:www-data /var/www/gestao_erp
sudo chmod -R 755 /var/www/gestao_erp
sudo chmod -R 644 /var/www/gestao_erp/media
```

### Erro: "Connection refused" ao conectar ao PostgreSQL

```bash
# Verificar se PostgreSQL esta rodando
sudo systemctl status postgresql

# Verificar se a porta 5432 esta aberta
sudo netstat -tlnp | grep 5432
```

### Erro: "502 Bad Gateway" no Nginx

```bash
# Verificar se Gunicorn esta rodando
sudo systemctl status gunicorn

# Verificar logs do Gunicorn
sudo journalctl -u gunicorn -n 50
```

---

**Desenvolvido por**: Manus AI  
**Data**: 07 de Fevereiro de 2026
