from django.test import TestCase, Client
from django.contrib.auth.models import User
from companies.models import Company, UserCompany
from estoque.models import Produto
from decimal import Decimal

class MultiTenancyTest(TestCase):
    """
    Testes para validar o isolamento de dados entre empresas.
    """
    
    def setUp(self):
        # Criar usuários
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        # Criar empresas
        self.company1 = Company.objects.create(
            nome='Empresa A', 
            cnpj='11.111.111/0001-11', 
            admin_principal=self.user1
        )
        self.company2 = Company.objects.create(
            nome='Empresa B', 
            cnpj='22.222.222/0001-22', 
            admin_principal=self.user2
        )
        
        # Associar usuários às empresas
        UserCompany.objects.create(user=self.user1, company=self.company1, role='ADMIN')
        UserCompany.objects.create(user=self.user2, company=self.company2, role='ADMIN')
        
        # Criar produtos para cada empresa
        self.product1 = Produto.objects.create(
            company=self.company1,
            nome='Produto Empresa A',
            sku='SKU-A',
            preco_custo=Decimal('10.00'),
            preco_venda=Decimal('20.00'),
            estoque_atual=100,
            usuario_criacao=self.user1
        )
        
        self.product2 = Produto.objects.create(
            company=self.company2,
            nome='Produto Empresa B',
            sku='SKU-B',
            preco_custo=Decimal('15.00'),
            preco_venda=Decimal('30.00'),
            estoque_atual=50,
            usuario_criacao=self.user2
        )

    def test_product_isolation(self):
        """
        Valida que cada empresa só vê seus próprios produtos.
        """
        # Produtos da Empresa A
        products_a = Produto.objects.filter(company=self.company1)
        self.assertEqual(products_a.count(), 1)
        self.assertEqual(products_a.first().nome, 'Produto Empresa A')
        
        # Produtos da Empresa B
        products_b = Produto.objects.filter(company=self.company2)
        self.assertEqual(products_b.count(), 1)
        self.assertEqual(products_b.first().nome, 'Produto Empresa B')

    def test_sku_uniqueness_per_company(self):
        """
        Valida que o SKU é único por empresa, mas pode ser repetido em empresas diferentes.
        """
        # Tentar criar produto com mesmo SKU na mesma empresa deve falhar
        from django.db import IntegrityError, transaction
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Produto.objects.create(
                    company=self.company1,
                    nome='Outro Produto Empresa A',
                    sku='SKU-A',
                    preco_custo=Decimal('5.00'),
                    preco_venda=Decimal('10.00'),
                    usuario_criacao=self.user1
                )
            
        # Criar produto com mesmo SKU em empresa diferente deve funcionar
        product_same_sku = Produto.objects.create(
            company=self.company2,
            nome='Produto Empresa B com SKU igual ao A',
            sku='SKU-A',
            preco_custo=Decimal('5.00'),
            preco_venda=Decimal('10.00'),
            usuario_criacao=self.user2
        )
        self.assertEqual(product_same_sku.sku, 'SKU-A')
        self.assertEqual(product_same_sku.company, self.company2)

from django.conf import settings

class SecurityTest(TestCase):
    """
    Testes para validar configurações de segurança.
    """
    
    def test_settings_load_from_env(self):
        """
        Valida que as configurações estão sendo carregadas corretamente.
        """
        # O valor do settings.DEBUG no ambiente de teste pode ser True por padrão do Django,
        # mas validamos se a SECRET_KEY não é a padrão de desenvolvimento hardcoded.
        self.assertNotEqual(settings.SECRET_KEY, 'django-insecure-r_e%n-0@n8fit$xx3c+p-%g(%p$36+#@zr%7%p#+jx0j#abta%')
        self.assertTrue(len(settings.SECRET_KEY) > 20)
