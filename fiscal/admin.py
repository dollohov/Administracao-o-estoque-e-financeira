"""
Configuração do Django Admin para o módulo Fiscal.

Autor: Manus AI
Data: 2026-02-05
"""

from django.contrib import admin
from .models import Fornecedor, NotaFiscalEletronica, ItemNotaFiscal


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    """Admin para Fornecedores."""
    list_display = ['razao_social', 'nome_fantasia', 'cnpj', 'cidade', 'estado', 'ativo']
    list_filter = ['ativo', 'estado']
    search_fields = ['razao_social', 'nome_fantasia', 'cnpj']
    ordering = ['razao_social']


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
