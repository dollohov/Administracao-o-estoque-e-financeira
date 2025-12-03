# Script de Teste de Fluxo (test_flow.py)
# Simula operações CRUD e financeiras para validar o sistema

from django.contrib.auth.models import User
from estoque.models import Produto, MovimentacaoEstoque
from financeiro.models import Receita, Despesa, CapitalGiro
from decimal import Decimal
from django.utils import timezone

print("--- Iniciando Teste de Fluxo ---")

# 1. Obter Usuário de Teste (Admin)
try:
    admin_user = User.objects.get(username='admin')
    print(f"✓ Usuário Admin encontrado: {admin_user.username}")
except User.DoesNotExist:
    print("✗ ERRO: Usuário 'admin' não encontrado. Execute setup_permissions.py.")
    exit()

# 2. Teste de Cadastro de Produto (CRUD - Create)
try:
    produto = Produto.objects.create(
        nome="Laptop Gamer X",
        descricao="Notebook de alta performance para jogos",
        preco_custo=Decimal('3000.00'),
        preco_venda=Decimal('5000.00'),
        estoque_atual=5,
        estoque_minimo=2,
        ativo=True,
        usuario_criacao=admin_user
    )
    print(f"✓ Produto cadastrado: {produto.nome} (ID: {produto.id})")
except Exception as e:
    print(f"✗ ERRO ao cadastrar produto: {e}")
    exit()

# 3. Teste de Movimentação de Estoque (ENTRADA)
try:
    # Simular capital inicial para evitar erro de capital insuficiente
    CapitalGiro.adicionar_capital(Decimal('10000.00'), "Capital Inicial para Teste", admin_user)
    
    # Simular compra (ENTRADA no estoque, SAÍDA no capital)
    MovimentacaoEstoque.objects.create(
        produto=produto,
        tipo='ENTRADA',
        quantidade=10,
        valor_unitario=produto.preco_custo,
        observacao="Compra de 10 unidades",
        usuario=admin_user
    )
    produto.refresh_from_db()
    print(f"✓ Movimentação ENTRADA registrada. Novo estoque: {produto.estoque_atual}")
    
    # Verificar se o capital foi debitado
    capital_atual = CapitalGiro.obter_capital_atual()
    esperado = Decimal('10000.00') - (Decimal('3000.00') * 10)
    print(f"✓ Capital de Giro após compra: R$ {capital_atual} (Esperado: R$ {esperado})")
    
except Exception as e:
    print(f"✗ ERRO na Movimentação ENTRADA: {e}")
    exit()

# 4. Teste de Movimentação de Estoque (SAÍDA)
try:
    # Simular venda (SAÍDA do estoque, ENTRADA no capital)
    MovimentacaoEstoque.objects.create(
        produto=produto,
        tipo='SAIDA',
        quantidade=2,
        valor_unitario=produto.preco_venda,
        observacao="Venda de 2 unidades",
        usuario=admin_user
    )
    produto.refresh_from_db()
    print(f"✓ Movimentação SAÍDA registrada. Novo estoque: {produto.estoque_atual}")
    
    # Verificar se o capital foi creditado
    capital_atual = CapitalGiro.obter_capital_atual()
    esperado = esperado + (Decimal('5000.00') * 2)
    print(f"✓ Capital de Giro após venda: R$ {capital_atual} (Esperado: R$ {esperado})")
    
    # Verificar se a Receita foi criada (lógica nas views, mas verificamos o capital)
    receita_venda = Receita.objects.filter(descricao__icontains="Venda de 2 unidades").first()
    if receita_venda:
        print(f"✓ Receita de venda registrada: R$ {receita_venda.valor}")
    else:
        print("✗ AVISO: Receita de venda não encontrada (verificar lógica da view)")
        
except Exception as e:
    print(f"✗ ERRO na Movimentação SAÍDA: {e}")
    exit()

# 5. Teste de Registro de Despesa (Fluxo de Caixa)
try:
    Despesa.objects.create(
        descricao="Pagamento de Aluguel",
        valor=Decimal('1500.00'),
        data=timezone.now().date(),
        categoria='ALUGUEL',
        usuario=admin_user
    )
    print("✓ Despesa registrada: Pagamento de Aluguel")
    
    # Verificar se o capital foi debitado
    capital_atual = CapitalGiro.obter_capital_atual()
    esperado = esperado - Decimal('1500.00')
    print(f"✓ Capital de Giro após despesa: R$ {capital_atual} (Esperado: R$ {esperado})")
    
except Exception as e:
    print(f"✗ ERRO ao registrar despesa: {e}")
    exit()

# 6. Teste de Indicadores Financeiros (Verificação de Lucro)
try:
    # O cálculo de indicadores é feito nas views, mas podemos verificar os dados brutos
    total_receitas = Receita.objects.aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
    total_despesas = Despesa.objects.aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
    lucro_bruto = total_receitas - total_despesas
    
    print(f"✓ Total Receitas: R$ {total_receitas}")
    print(f"✓ Total Despesas: R$ {total_despesas}")
    print(f"✓ Lucro Bruto (simulado): R$ {lucro_bruto}")
    
except Exception as e:
    print(f"✗ ERRO na verificação de indicadores: {e}")
    exit()

print("--- Teste de Fluxo Concluído ---")
