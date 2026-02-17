import os
import django
import secrets
import string

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.contrib.auth.models import User
from companies.models import Company, UserCompany

def init_system():
    # 1. Gerar senha segura
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(12))
    
    username = 'admin'
    email = 'admin@exemplo.com.br'
    
    # 2. Criar Empresa Padrão
    company, created = Company.objects.get_or_create(
        name="Minha Empresa ERP",
        defaults={'cnpj': '00.000.000/0001-00'}
    )
    
    # 3. Criar Superusuário
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username, email, password)
        print(f"✅ Usuário '{username}' criado com sucesso.")
    else:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✅ Senha do usuário '{username}' atualizada.")
        
    # 4. Vincular Usuário à Empresa
    UserCompany.objects.get_or_create(
        user=user, 
        company=company, 
        defaults={'role': 'ADMIN'}
    )
    
    print(f"--- CREDENCIAIS DE ACESSO ---")
    print(f"URL: Seu link no Render")
    print(f"Usuário: {username}")
    print(f"Senha: {password}")
    print(f"Empresa: {company.name}")
    print(f"-----------------------------")
    
    # Salvar em arquivo temporário para leitura pelo Manus
    with open('/home/ubuntu/admin_creds.txt', 'w') as f:
        f.write(f"USER: {username}\nPASS: {password}\nCOMPANY: {company.name}")

if __name__ == "__main__":
    init_system()
