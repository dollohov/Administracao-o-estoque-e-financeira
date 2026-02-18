import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.contrib.auth.models import User
from companies.models import Company, UserCompany

def create_admin():
    username = 'admin'
    password = 'admin123'
    email = 'admin@exemplo.com.br'
    
    company, _ = Company.objects.get_or_create(
        name="Minha Empresa ERP",
        defaults={'cnpj': '00.000.000/0001-00'}
    )
    
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'is_superuser': True, 'is_staff': True}
    )
    
    user.set_password(password)
    user.save()
    
    UserCompany.objects.get_or_create(
        user=user, 
        company=company, 
        defaults={'role': 'ADMIN'}
    )
    
    print(f"✅ Usuário '{username}' com senha '{password}' garantido.")

if __name__ == "__main__":
    create_admin()
