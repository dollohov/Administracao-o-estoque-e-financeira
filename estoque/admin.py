"""
Configuração do painel de administração do Django para o módulo de Estoque.

Este arquivo personaliza a interface administrativa para os modelos
Produto e MovimentacaoEstoque, facilitando o gerenciamento via painel admin.

Autor: Manus AI
Data: 2025-12-02
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Produto, MovimentacaoEstoque


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """
    Configuração administrativa para o modelo Produto.
    
    Personaliza a exibição e funcionalidades do modelo Produto
    no painel de administração do Django com campos fiscais e logísticos.
    """
    
    # Campos exibidos na listagem
    list_display = [
        'nome_com_sku',
        'preco_venda',
        'estoque_com_alerta',
        'ncm',
        'categoria',
        'visivel_catalogo',
        'ativo',
        'data_criacao'
    ]
    
    # Campos que podem ser usados para filtrar
    list_filter = [
        'ativo',
        'visivel_catalogo',
        'categoria',
        'marca',
        'data_criacao',
        'usuario_criacao'
    ]
    
    # Campos de busca (incluindo campos fiscais)
    search_fields = [
        'nome',
        'sku',
        'ncm',
        'ean_gtin',
        'descricao',
        'categoria',
        'marca'
    ]
    
    # Campos somente leitura (não editáveis)
    readonly_fields = [
        'usuario_criacao',
        'data_criacao',
        'usuario_modificacao',
        'data_modificacao',
        'volume_m3',
        'margem_lucro_display',
        'valor_estoque_display'
    ]
    
    # Organização dos campos no formulário em abas
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'marca', 'categoria', 'subcategoria')
        }),
        ('Identificação e Códigos', {
            'fields': ('sku', 'ncm', 'cest', 'ean_gtin'),
            'description': 'Códigos fiscais e de identificação obrigatórios para NF-e'
        }),
        ('Precificação', {
            'fields': ('preco_custo', 'preco_venda', 'margem_lucro_display')
        }),
        ('Controle de Estoque', {
            'fields': (
                'estoque_atual',
                'estoque_minimo',
                'estoque_maximo',
                'valor_estoque_display'
            ),
            'description': 'Controle de quantidades e alertas de reposição'
        }),
        ('Dimensões e Logística', {
            'fields': (
                'peso_kg',
                'altura_cm',
                'largura_cm',
                'profundidade_cm',
                'volume_m3'
            ),
            'classes': ('collapse',),
            'description': 'Informações para cálculo de frete e armazenamento'
        }),
        ('Localização no Estoque', {
            'fields': ('localizacao_estoque',),
            'classes': ('collapse',)
        }),
        ('Impostos', {
            'fields': (
                'icms_aliquota',
                'ipi_aliquota',
                'pis_aliquota',
                'cofins_aliquota'
            ),
            'classes': ('collapse',),
            'description': 'Alíquotas de impostos para cálculo fiscal'
        }),
        ('Fornecedor e Catálogo', {
            'fields': ('fornecedor', 'imagem', 'visivel_catalogo')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Rastreamento', {
            'fields': (
                'usuario_criacao',
                'data_criacao',
                'usuario_modificacao',
                'data_modificacao'
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Ordenação padrão
    ordering = ['nome']
    
    # Número de itens por página
    list_per_page = 25
    
    # Campos com autocompletar
    autocomplete_fields = ['fornecedor']
    
    def nome_com_sku(self, obj):
        """Exibe o nome do produto com o SKU."""
        if obj.sku:
            return f"{obj.nome} ({obj.sku})"
        return obj.nome
    nome_com_sku.short_description = "Produto"
    
    def estoque_com_alerta(self, obj):
        """Exibe o estoque com alerta visual se estiver baixo."""
        if obj.estoque_baixo():
            return format_html(
                '<span style="color: red; font-weight: bold;">{} ⚠️</span>',
                obj.estoque_atual
            )
        elif obj.estoque_alto():
            return format_html(
                '<span style="color: orange;">{} ℹ️</span>',
                obj.estoque_atual
            )
        return format_html(
            '<span style="color: green;">{} ✓</span>',
            obj.estoque_atual
        )
    estoque_com_alerta.short_description = "Estoque"
    
    def margem_lucro_display(self, obj):
        """Exibe a margem de lucro formatada."""
        margem = obj.calcular_margem_lucro()
        return format_html(
            '<strong>{:.2f}%</strong>',
            margem
        )
    margem_lucro_display.short_description = "Margem de Lucro"
    
    def valor_estoque_display(self, obj):
        """Exibe o valor total do estoque."""
        valor = obj.valor_total_estoque()
        return format_html(
            '<strong>R$ {:.2f}</strong>',
            valor
        )
    valor_estoque_display.short_description = "Valor Total em Estoque"
    
    def save_model(self, request, obj, form, change):
        """
        Sobrescreve o método de salvamento para registrar o usuário.
        
        Args:
            request: Objeto HttpRequest
            obj: Instância do modelo sendo salva
            form: Formulário com os dados
            change: Boolean indicando se é uma edição (True) ou criação (False)
        """
        if not change:
            # Se é um novo registro, define o usuário de criação
            obj.usuario_criacao = request.user
        else:
            # Se é uma edição, atualiza o usuário de modificação
            obj.usuario_modificacao = request.user
        
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Otimiza a query com select_related para fornecedor."""
        queryset = super().get_queryset(request)
        return queryset.select_related('fornecedor', 'usuario_criacao')


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    """
    Configuração administrativa para o modelo MovimentacaoEstoque.
    
    Personaliza a exibição das movimentações de estoque no painel admin.
    """
    
    # Campos exibidos na listagem
    list_display = [
        'produto',
        'tipo_com_cor',
        'quantidade',
        'valor_unitario',
        'valor_total_display',
        'usuario',
        'data_movimentacao'
    ]
    
    # Campos que podem ser usados para filtrar
    list_filter = [
        'tipo',
        'data_movimentacao',
        'usuario',
        'produto__categoria'
    ]
    
    # Campos de busca
    search_fields = [
        'produto__nome',
        'produto__sku',
        'observacao',
        'usuario__username'
    ]
    
    # Campos somente leitura
    readonly_fields = [
        'usuario',
        'data_movimentacao',
        'valor_total_display'
    ]
    
    # Organização dos campos no formulário
    fieldsets = (
        ('Movimentação', {
            'fields': ('produto', 'tipo', 'quantidade', 'valor_unitario', 'valor_total_display')
        }),
        ('Observações', {
            'fields': ('observacao',)
        }),
        ('Rastreamento', {
            'fields': ('usuario', 'data_movimentacao'),
            'classes': ('collapse',)
        }),
    )
    
    # Ordenação padrão (mais recentes primeiro)
    ordering = ['-data_movimentacao']
    
    # Número de itens por página
    list_per_page = 50
    
    # Campos com autocompletar (melhora performance com muitos registros)
    autocomplete_fields = ['produto']
    
    def tipo_com_cor(self, obj):
        """Exibe o tipo de movimentação com cores."""
        if obj.tipo == 'ENTRADA':
            return format_html(
                '<span style="color: green; font-weight: bold;">↓ ENTRADA</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">↑ SAÍDA</span>'
            )
    tipo_com_cor.short_description = "Tipo"
    
    def valor_total_display(self, obj):
        """Exibe o valor total da movimentação."""
        valor = obj.calcular_valor_total()
        return format_html(
            '<strong>R$ {:.2f}</strong>',
            valor
        )
    valor_total_display.short_description = "Valor Total"
    
    def save_model(self, request, obj, form, change):
        """
        Sobrescreve o método de salvamento para registrar o usuário.
        
        Args:
            request: Objeto HttpRequest
            obj: Instância do modelo sendo salva
            form: Formulário com os dados
            change: Boolean indicando se é uma edição (True) ou criação (False)
        """
        if not change:
            # Define o usuário responsável pela movimentação
            obj.usuario = request.user
        
        super().save_model(request, obj, form, change)
    
    def has_delete_permission(self, request, obj=None):
        """
        Restringe a exclusão de movimentações.
        
        Apenas superusuários podem excluir movimentações para manter
        a integridade do histórico.
        
        Args:
            request: Objeto HttpRequest
            obj: Instância do modelo (opcional)
            
        Returns:
            bool: True se pode excluir, False caso contrário
        """
        return request.user.is_superuser
    
    def get_queryset(self, request):
        """Otimiza a query com select_related."""
        queryset = super().get_queryset(request)
        return queryset.select_related('produto', 'usuario')
