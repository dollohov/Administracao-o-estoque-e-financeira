"""
Configuração do painel de administração para o módulo de Fornecedores.

Autor: Manus AI
Data: 2025-12-02
"""

from django.contrib import admin
from .models import Fornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    """
    Configuração administrativa para o modelo Fornecedor.
    """
    
    # Campos exibidos na listagem
    list_display = [
        'nome',
        'cnpj',
        'email',
        'telefone',
        'cidade',
        'estado',
        'ativo',
        'data_criacao'
    ]
    
    # Campos que podem ser usados para filtrar
    list_filter = [
        'ativo',
        'estado',
        'data_criacao',
        'usuario_criacao'
    ]
    
    # Campos de busca
    search_fields = [
        'nome',
        'cnpj',
        'email',
        'telefone',
        'cidade'
    ]
    
    # Campos somente leitura
    readonly_fields = [
        'usuario_criacao',
        'data_criacao',
        'usuario_modificacao',
        'data_modificacao'
    ]
    
    # Organização dos campos no formulário
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Documentação', {
            'fields': ('cnpj',)
        }),
        ('Endereço', {
            'fields': ('endereco', 'cidade', 'estado', 'cep')
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
    
    def save_model(self, request, obj, form, change):
        """Registra o usuário de criação/modificação."""
        if not change:
            obj.usuario_criacao = request.user
        else:
            obj.usuario_modificacao = request.user
        
        super().save_model(request, obj, form, change)
