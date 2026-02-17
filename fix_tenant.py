
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestao_erp.settings")
django.setup()

from django.contrib.auth.models import User
from companies.models import Company, UserCompany

def fix():
    # 1. Obter ou criar o usuário admin
    admin = User.objects.filter(username='admin').first()
    if not admin:
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superusuário 'admin' criado.")
    else:
        print("Superusuário 'admin' já existe.")

    # 2. Obter ou criar uma empresa de teste
    company, created = Company.objects.get_or_create(
        cnpj='12.345.678/0001-99',
        defaults={'name': 'Empresa de Teste', 'active': True}
    )
    if created:
        print(f"Empresa '{company.name}' criada.")
    else:
        print(f"Empresa '{company.name}' já existe.")

    # 3. Vincular admin à empresa
    user_company, created = UserCompany.objects.get_or_create(
        user=admin,
        company=company,
        defaults={'role': 'ADMIN'}
    )
    if created:
        print(f"Usuário 'admin' vinculado à empresa '{company.name}' como ADMIN.")
    else:
        print(f"Usuário 'admin' já está vinculado à empresa '{company.name}'.")

if __name__ == "__main__":
    fix()
