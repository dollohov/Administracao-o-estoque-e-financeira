import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_erp.settings')
django.setup()

from django.contrib.auth.models import User
from companies.models import Company, UserCompany

def auto_init():
    # 1. Criar Empresa Padrão se não existir
    company, created = Company.objects.get_or_create(
        name="Minha Empresa ERP",
        defaults={'cnpj': '00.000.000/0001-00'}
    )
    if created:
        print(f"✅ Empresa '{company.name}' criada.")
    
    # 2. Lista de Superusuários para garantir acesso
    superusers = [
        {'username': 'denisbarbosa', 'password': 'denis123', 'email': 'denis@exemplo.com.br'},
        {'username': 'admin', 'password': 'admin123', 'email': 'admin@exemplo.com.br'}
    ]
    
    for su in superusers:
        user, created = User.objects.get_or_create(
            username=su['username'],
            defaults={'email': su['email'], 'is_superuser': True, 'is_staff': True}
        )
        
        # Garante a senha em ambos os casos (novo ou existente)
        user.set_password(su['password'])
        user.save()
        
        status = "criado" if created else "atualizado"
        print(f"✅ Superusuário '{su['username']}' {status} com sucesso.")
        
        # 3. Garantir vínculo do Usuário com a Empresa
        UserCompany.objects.get_or_create(
            user=user, 
            company=company, 
            defaults={'role': 'ADMIN'}
        )
        print(f"✅ Vínculo do usuário '{su['username']}' com a empresa garantido.")

if __name__ == "__main__":
    try:
        auto_init()
    except Exception as e:
        print(f"⚠️ Erro na inicialização automática: {e}")
