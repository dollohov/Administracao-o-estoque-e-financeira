"""
Configuração do Django Admin para o módulo Fiscal.

Autor: Manus AI
Data: 2026-02-05
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Fornecedor, NotaFiscalEletronica, ItemNotaFiscal, ProdutoFiscal


@admin.register(ProdutoFiscal)
class ProdutoFiscalAdmin(admin.ModelAdmin):
    """
    Configuração administrativa para o modelo Produto dentro do módulo Fiscal.
    
    Replica a interface de modificação de produtos do estoque para o módulo fiscal.
    """
    
    # Campos exibidos na listagem
    list_display = [
        'nome_com_sku',
        'preco_venda',
        'ncm',
        'cest',
        'ean_gtin',
        'categoria',
        'ativo'
    ]
    
    # Campos que podem ser usados para filtrar
    list_filter = [
        'ativo',
        'categoria',
        'marca',
        'data_criacao'
    ]
    
    # Campos de busca
    search_fields = [
        'nome',
        'sku',
        'ncm',
        'ean_gtin',
        'descricao'
    ]
    
    # Campos somente leitura
    readonly_fields = [
        'usuario_criacao',
        'data_criacao',
        'usuario_modificacao',
        'data_modificacao',
        'volume_m3',
        'margem_lucro_display',
        'valor_estoque_display'
    ]
    
    # Organização dos campos no formulário (Foco em Identificação e Códigos)
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
        ('Impostos', {
            'fields': (
                'icms_aliquota',
                'ipi_aliquota',
                'pis_aliquota',
                'cofins_aliquota'
            ),
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
    
    ordering = ['nome']
    list_per_page = 25
    autocomplete_fields = ['fornecedor']
    
    def nome_com_sku(self, obj):
        if obj.sku:
            return f"{obj.nome} ({obj.sku})"
        return obj.nome
    nome_com_sku.short_description = "Produto"
    
    def margem_lucro_display(self, obj):
        margem = obj.calcular_margem_lucro()
        return format_html('<strong>{:.2f}%</strong>', margem)
    margem_lucro_display.short_description = "Margem de Lucro"
    
    def valor_estoque_display(self, obj):
        valor = obj.valor_total_estoque()
        return format_html('<strong>R$ {:.2f}</strong>', valor)
    valor_estoque_display.short_description = "Valor Total em Estoque"
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario_criacao = request.user
        else:
            obj.usuario_modificacao = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('fornecedor', 'usuario_criacao')


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    """Admin para Fornecedores."""
    list_display = ['razao_social', 'nome_fantasia', 'cnpj', 'cidade', 'estado', 'ativo']
    list_filter = ['ativo', 'estado']
    search_fields = ['razao_social', 'nome_fantasia', 'cnpj']
    ordering = ['razao_social']
    search_fields = ['razao_social', 'cnpj'] # Necessário para autocomplete


class ItemNotaFiscalInline(admin.TabularInline):
    """Inline para itens da NF-e."""
    model = ItemNotaFiscal
    extra = 0
    readonly_fields = ['numero_item', 'codigo_produto', 'descricao', 'quantidade', 
                      'valor_unitario', 'valor_total']


@admin.register(NotaFiscalEletronica)
class NotaFiscalEletronicaAdmin(admin.ModelAdmin):
    """Admin para Notas Fiscais Eletrônicas."""
    list_display = ['numero', 'serie', 'fornecedor', 'data_emissao', 'valor_total', 
                   'status', 'data_importacao']
    list_filter = ['status', 'data_emissao', 'data_importacao']
    search_fields = ['numero', 'chave_acesso', 'fornecedor__razao_social']
    readonly_fields = ['chave_acesso', 'data_importacao', 'usuario_importacao']
    inlines = [ItemNotaFiscalInline]
    ordering = ['-data_emissao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('chave_acesso', 'numero', 'serie', 'fornecedor', 'data_emissao')
        }),
        ('Valores', {
            'fields': ('valor_produtos', 'valor_total', 'valor_icms', 'valor_ipi', 
                      'valor_pis', 'valor_cofins', 'valor_frete', 'valor_desconto')
        }),
        ('Informações Fiscais', {
            'fields': ('natureza_operacao', 'cfop')
        }),
        ('Status e Observações', {
            'fields': ('status', 'observacoes', 'xml_arquivo')
        }),
        ('Rastreamento', {
            'fields': ('usuario_importacao', 'data_importacao')
        }),
    )


@admin.register(ItemNotaFiscal)
class ItemNotaFiscalAdmin(admin.ModelAdmin):
    """Admin para Itens de Nota Fiscal."""
    list_display = ['nota_fiscal', 'numero_item', 'descricao', 'quantidade', 
                   'valor_unitario', 'valor_total']
    list_filter = ['nota_fiscal__status', 'criado_automaticamente']
    search_fields = ['descricao', 'codigo_produto', 'nota_fiscal__numero']
    ordering = ['nota_fiscal', 'numero_item']
