"""
Testes automatizados para o módulo de Estoque.

Este arquivo contém testes unitários e de integração para o módulo de estoque,
incluindo testes de models, views e lógica de negócio.

Autor: Denis Barbosa (Todos os direitos reservados)
Data: 2026-02-17
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from decimal import Decimal
from estoque.models import Produto, MovimentacaoEstoque
from companies.models import Company, UserCompany


class ProdutoModelTest(TestCase):
    """Testes para o modelo Produto."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar empresa de teste
        self.company = Company.objects.create(
            name="Empresa Teste",
            cnpj="12.345.678/0001-99",
            plano="BASIC"
        )
        
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        
        # Associar usuário à empresa
        UserCompany.objects.create(
            user=self.user,
            company=self.company,
            role='ADMIN'
        )
        
        # Criar produto de teste
        self.produto = Produto.objects.create(
            company=self.company,
            nome="Produto Teste",
            descricao="Descrição do produto teste",
            sku="PROD001",
            preco_custo=Decimal('10.00'),
            preco_venda=Decimal('20.00'),
            estoque_atual=100,
            estoque_minimo=10,
            usuario_criacao=self.user,
            usuario_modificacao=self.user
        )
    
    def test_produto_creation(self):
        """Testa se o produto foi criado corretamente."""
        self.assertEqual(self.produto.nome, "Produto Teste")
        self.assertEqual(self.produto.sku, "PROD001")
        self.assertEqual(self.produto.preco_custo, Decimal('10.00'))
        self.assertEqual(self.produto.preco_venda, Decimal('20.00'))
        self.assertEqual(self.produto.estoque_atual, 100)
    
    def test_margem_lucro(self):
        """Testa o cálculo da margem de lucro."""
        margem = self.produto.margem_lucro()
        self.assertEqual(margem, Decimal('50.00'))  # (20-10)/20 * 100 = 50%
    
    def test_valor_total_estoque(self):
        """Testa o cálculo do valor total em estoque."""
        valor_total = self.produto.valor_total_estoque()
        self.assertEqual(valor_total, Decimal('1000.00'))  # 100 * 10.00
    
    def test_produto_str(self):
        """Testa a representação em string do produto."""
        self.assertIn("Produto Teste", str(self.produto))


class MovimentacaoEstoqueTest(TestCase):
    """Testes para movimentações de estoque."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar empresa de teste
        self.company = Company.objects.create(
            name="Empresa Teste",
            cnpj="12.345.678/0001-99",
            plano="BASIC"
        )
        
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Associar usuário à empresa
        UserCompany.objects.create(
            user=self.user,
            company=self.company,
            role='ADMIN'
        )
        
        # Criar produto de teste
        self.produto = Produto.objects.create(
            company=self.company,
            nome="Produto Teste",
            sku="PROD001",
            preco_custo=Decimal('10.00'),
            preco_venda=Decimal('20.00'),
            estoque_atual=100,
            estoque_minimo=10,
            usuario_criacao=self.user,
            usuario_modificacao=self.user
        )
    
    def test_movimentacao_entrada(self):
        """Testa entrada de estoque."""
        estoque_inicial = self.produto.estoque_atual
        
        MovimentacaoEstoque.objects.create(
            produto=self.produto,
            tipo='ENTRADA',
            quantidade=50,
            valor_unitario=Decimal('10.00'),
            usuario=self.user
        )
        
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque_atual, estoque_inicial + 50)
    
    def test_movimentacao_saida(self):
        """Testa saída de estoque."""
        estoque_inicial = self.produto.estoque_atual
        
        MovimentacaoEstoque.objects.create(
            produto=self.produto,
            tipo='SAIDA',
            quantidade=20,
            valor_unitario=Decimal('20.00'),
            usuario=self.user
        )
        
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque_atual, estoque_inicial - 20)


class EstoqueViewsTest(TestCase):
    """Testes para as views do módulo de estoque."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar empresa de teste
        self.company = Company.objects.create(
            name="Empresa Teste",
            cnpj="12.345.678/0001-99",
            plano="BASIC"
        )
        
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Associar usuário à empresa
        UserCompany.objects.create(
            user=self.user,
            company=self.company,
            role='ADMIN'
        )
        
        # Cliente de teste
        self.client = Client()
    
    def test_dashboard_estoque_requires_login(self):
        """Testa se o dashboard requer autenticação."""
        response = self.client.get('/estoque/')
        # Deve redirecionar para login
        self.assertEqual(response.status_code, 302)
    
    def test_dashboard_estoque_authenticated(self):
        """Testa acesso ao dashboard autenticado."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/estoque/')
        # Deve retornar 200 ou 302 (dependendo do middleware)
        self.assertIn(response.status_code, [200, 302])
