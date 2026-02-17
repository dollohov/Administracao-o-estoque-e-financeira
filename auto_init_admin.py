import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.contrib.auth.models import User
from companies.models import Company, UserCompany

def auto_init():
    username = 'admin'
    password = 'admin123'
    email = 'admin@exemplo.com.br'
    
    # 1. Criar Empresa Padrão se não existir
    company, created = Company.objects.get_or_create(
        name="Minha Empresa ERP",
        defaults={'cnpj': '00.000.000/0001-00'}
    )
    if created:
        print(f"✅ Empresa '{company.name}' criada.")
    
    # 2. Criar ou atualizar Superusuário
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'is_superuser': True, 'is_staff': True}
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"✅ Superusuário '{username}' criado com sucesso.")
    else:
        # Garante que a senha seja admin123 para o primeiro acesso se o usuário já existia
        user.set_password(password)
        user.save()
        print(f"✅ Senha do superusuário '{username}' atualizada para 'admin123'.")
        
    # 3. Garantir vínculo do Usuário com a Empresa
    UserCompany.objects.get_or_create(
        user=user, 
        company=company, 
        defaults={'role': 'ADMIN'}
    )
    print("✅ Vínculo usuário-empresa garantido.")

if __name__ == "__main__":
    try:
        auto_init()
    except Exception as e:
        print(f"⚠️ Erro na inicialização automática: {e}")
