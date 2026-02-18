import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.contrib.auth.models import User
from companies.models import Company, UserCompany

def create_admin():
    company, _ = Company.objects.get_or_create(
        name="Minha Empresa ERP",
        defaults={'cnpj': '00.000.000/0001-00'}
    )
    
    superusers = [
        {'username': 'denisbarbosa', 'password': 'denis123', 'email': 'denis@exemplo.com.br'},
        {'username': 'admin', 'password': 'admin123', 'email': 'admin@exemplo.com.br'}
    ]
    
    for su in superusers:
        user, created = User.objects.get_or_create(
            username=su['username'],
            defaults={'email': su['email'], 'is_superuser': True, 'is_staff': True}
        )
        
        user.set_password(su['password'])
        user.save()
        
        UserCompany.objects.get_or_create(
            user=user, 
            company=company, 
            defaults={'role': 'ADMIN'}
        )
        
        print(f"✅ Usuário '{su['username']}' com senha '{su['password']}' garantido.")

if __name__ == "__main__":
    create_admin()
