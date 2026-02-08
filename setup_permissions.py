from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from estoque.models import Produto, MovimentacaoEstoque
from financeiro.models import Receita, Despesa, CapitalGiro
from fiscal.models import NotaFiscalEletronica, Fornecedor
from clientes.models import Cliente
from vendas.models import Pedido, ItemPedido

def setup_permissions():
    # ==========================================================================
    # GRUPOS DE USUÁRIOS
    # ==========================================================================
    admin_group, created = Group.objects.get_or_create(name="Administradores")
    gerente_group, created = Group.objects.get_or_create(name="Gerentes")
    funcionario_group, created = Group.objects.get_or_create(name="Funcionários")
    vendedor_group, created = Group.objects.get_or_create(name="Vendedores")

    # ==========================================================================
    # PERMISSÕES GERAIS
    # ==========================================================================
    # Content Types
    ct_produto = ContentType.objects.get_for_model(Produto)
    ct_movimentacao = ContentType.objects.get_for_model(MovimentacaoEstoque)
    ct_receita = ContentType.objects.get_for_model(Receita)
    ct_despesa = ContentType.objects.get_for_model(Despesa)
    ct_capital_giro = ContentType.objects.get_for_model(CapitalGiro)
    ct_nfe = ContentType.objects.get_for_model(NotaFiscalEletronica)
    ct_fornecedor = ContentType.objects.get_for_model(Fornecedor)
    ct_cliente = ContentType.objects.get_for_model(Cliente)
    ct_pedido = ContentType.objects.get_for_model(Pedido)
    ct_item_pedido = ContentType.objects.get_for_model(ItemPedido)

    # Permissões de Estoque
    perm_view_produto = Permission.objects.get(codename="view_produto", content_type=ct_produto)
    perm_add_produto = Permission.objects.get(codename="add_produto", content_type=ct_produto)
    perm_change_produto = Permission.objects.get(codename="change_produto", content_type=ct_produto)
    perm_delete_produto = Permission.objects.get(codename="delete_produto", content_type=ct_produto)
    perm_view_movimentacao = Permission.objects.get(codename="view_movimentacaoestoque", content_type=ct_movimentacao)
    perm_add_movimentacao = Permission.objects.get(codename="add_movimentacaoestoque", content_type=ct_movimentacao)

    # Permissões Financeiras
    perm_view_receita = Permission.objects.get(codename="view_receita", content_type=ct_receita)
    perm_add_receita = Permission.objects.get(codename="add_receita", content_type=ct_receita)
    perm_change_receita = Permission.objects.get(codename="change_receita", content_type=ct_receita)
    perm_view_despesa = Permission.objects.get(codename="view_despesa", content_type=ct_despesa)
    perm_add_despesa = Permission.objects.get(codename="add_despesa", content_type=ct_despesa)
    perm_change_despesa = Permission.objects.get(codename="change_despesa", content_type=ct_despesa)
    perm_view_capital_giro = Permission.objects.get(codename="view_capitalgiro", content_type=ct_capital_giro)

    # Permissões Fiscais
    perm_view_nfe = Permission.objects.get(codename="view_notafiscaleletronica", content_type=ct_nfe)
    perm_add_nfe = Permission.objects.get(codename="add_notafiscaleletronica", content_type=ct_nfe)
    perm_view_fornecedor = Permission.objects.get(codename="view_fornecedor", content_type=ct_fornecedor)
    perm_add_fornecedor = Permission.objects.get(codename="add_fornecedor", content_type=ct_fornecedor)
    perm_change_fornecedor = Permission.objects.get(codename="change_fornecedor", content_type=ct_fornecedor)

    # Permissões de Clientes
    perm_view_cliente = Permission.objects.get(codename="view_cliente", content_type=ct_cliente)
    perm_add_cliente = Permission.objects.get(codename="add_cliente", content_type=ct_cliente)
    perm_change_cliente = Permission.objects.get(codename="change_cliente", content_type=ct_cliente)

    # Permissões de Vendas (Novo)
    perm_view_pedido = Permission.objects.get(codename="view_pedido", content_type=ct_pedido)
    perm_add_pedido = Permission.objects.get(codename="add_pedido", content_type=ct_pedido)
    perm_change_pedido = Permission.objects.get(codename="change_pedido", content_type=ct_pedido)
    perm_delete_pedido = Permission.objects.get(codename="delete_pedido", content_type=ct_pedido)
    perm_view_item_pedido = Permission.objects.get(codename="view_itempedido", content_type=ct_item_pedido)

    # ==========================================================================
    # ATRIBUIR PERMISSÕES AOS GRUPOS
    # ==========================================================================

    # Administradores: Todas as permissões (geralmente via is_superuser, mas bom ter aqui)
    admin_group.permissions.set(Permission.objects.all())

    # Gerentes: Gestão completa (Estoque, Financeiro, Fiscal, Clientes, Fornecedores, Vendas)
    gerente_permissions = [
        perm_view_produto, perm_add_produto, perm_change_produto, perm_delete_produto,
        perm_view_movimentacao, perm_add_movimentacao,
        perm_view_receita, perm_add_receita, perm_change_receita,
        perm_view_despesa, perm_add_despesa, perm_change_despesa,
        perm_view_capital_giro,
        perm_view_nfe, perm_add_nfe,
        perm_view_fornecedor, perm_add_fornecedor, perm_change_fornecedor,
        perm_view_cliente, perm_add_cliente, perm_change_cliente,
        perm_view_pedido, perm_add_pedido, perm_change_pedido, perm_delete_pedido, perm_view_item_pedido,
    ]
    gerente_group.permissions.set(gerente_permissions)

    # Funcionários: Apenas visualização e movimentação de estoque
    funcionario_permissions = [
        perm_view_produto, perm_view_movimentacao, perm_add_movimentacao,
        perm_view_pedido, perm_add_pedido, perm_change_pedido, perm_view_item_pedido,
    ]
    funcionario_group.permissions.set(funcionario_permissions)

    # Vendedores: Apenas visualização de produtos (catálogo) e gestão de pedidos
    vendedor_permissions = [
        perm_view_produto,
        perm_view_pedido, perm_add_pedido, perm_change_pedido, perm_view_item_pedido,
        perm_view_cliente, perm_add_cliente, perm_change_cliente,
    ]
    vendedor_group.permissions.set(vendedor_permissions)

    print("Permissões e grupos configurados com sucesso!")
