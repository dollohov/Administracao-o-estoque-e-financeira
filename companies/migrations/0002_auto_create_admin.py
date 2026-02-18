from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_default_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Company = apps.get_model('companies', 'Company')
    UserCompany = apps.get_model('companies', 'UserCompany')

    # 1. Criar Empresa Padrão
    company, created = Company.objects.get_or_create(
        name="Minha Empresa ERP",
        defaults={'cnpj': '00.000.000/0001-00'}
    )

    # 2. Criar Superusuário
    username = 'admin'
    password = 'admin123'
    email = 'admin@exemplo.com.br'

    if not User.objects.filter(username=username).exists():
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_superuser=True,
            is_staff=True
        )
    else:
        user = User.objects.get(username=username)
        user.password = make_password(password)
        user.save()

    # 3. Vincular Usuário à Empresa
    UserCompany.objects.get_or_create(
        user=user, 
        company=company, 
        defaults={'role': 'ADMIN'}
    )

def remove_default_admin(apps, schema_editor):
    # Opcional: remover o usuário se a migração for revertida
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'), # Dependência da app auth
    ]

    operations = [
        migrations.RunPython(create_default_admin, remove_default_admin),
    ]
