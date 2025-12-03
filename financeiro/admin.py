"""
Configuração do painel de administração do Django para o módulo Financeiro.

Este arquivo personaliza a interface administrativa para os modelos
de Receita, Despesa, Capital de Giro e Indicadores Financeiros.

Autor: Manus AI
Data: 2025-12-02
"""

from django.contrib import admin
from .models import Receita, Despesa, CapitalGiro, IndicadorFinanceiro


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    """
    Configuração administrativa para o modelo Receita.
    
    Personaliza a exibição e funcionalidades do modelo Receita
    no painel de administração do Django.
    """
    
    # Campos exibidos na listagem
    list_display = [
        'descricao',
        'valor',
        'data',
        'categoria',
        'usuario',
        'data_criacao'
    ]
    
    # Campos que podem ser usados para filtrar
    list_filter = [
        'categoria',
        'data',
        'usuario'
    ]
    
    # Campos de busca
    search_fields = [
        'descricao'
    ]
    
    # Campos somente leitura
    readonly_fields = [
        'usuario',
        'data_criacao'
    ]
    
    # Organização dos campos no formulário
    fieldsets = (
        ('Informações da Receita', {
            'fields': ('descricao', 'valor', 'data', 'categoria')
        }),
        ('Rastreamento', {
            'fields': ('usuario', 'data_criacao'),
            'classes': ('collapse',)
        }),
    )
    
    # Ordenação padrão (mais recentes primeiro)
    ordering = ['-data']
    
    # Número de itens por página
    list_per_page = 50
    
    # Data padrão no formulário
    date_hierarchy = 'data'
    
    def save_model(self, request, obj, form, change):
        """
        Sobrescreve o método de salvamento para registrar o usuário.
        
        Args:
            request: Objeto HttpRequest
            obj: Instância do modelo sendo salva
            form: Formulário com os dados
            change: Boolean indicando se é uma edição
        """
        if not change:
            obj.usuario = request.user
        
        super().save_model(request, obj, form, change)


@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    """
    Configuração administrativa para o modelo Despesa.
    
    Personaliza a exibição e funcionalidades do modelo Despesa
    no painel de administração do Django.
    """
    
    # Campos exibidos na listagem
    list_display = [
        'descricao',
        'valor',
        'data',
        'categoria',
        'usuario',
        'data_criacao'
    ]
    
    # Campos que podem ser usados para filtrar
    list_filter = [
        'categoria',
        'data',
        'usuario'
    ]
    
    # Campos de busca
    search_fields = [
        'descricao'
    ]
    
    # Campos somente leitura
    readonly_fields = [
        'usuario',
        'data_criacao'
    ]
    
    # Organização dos campos no formulário
    fieldsets = (
        ('Informações da Despesa', {
            'fields': ('descricao', 'valor', 'data', 'categoria')
        }),
        ('Rastreamento', {
            'fields': ('usuario', 'data_criacao'),
            'classes': ('collapse',)
        }),
    )
    
    # Ordenação padrão (mais recentes primeiro)
    ordering = ['-data']
    
    # Número de itens por página
    list_per_page = 50
    
    # Data padrão no formulário
    date_hierarchy = 'data'
    
    def save_model(self, request, obj, form, change):
        """
        Sobrescreve o método de salvamento para registrar o usuário.
        
        Args:
            request: Objeto HttpRequest
            obj: Instância do modelo sendo salva
            form: Formulário com os dados
            change: Boolean indicando se é uma edição
        """
        if not change:
            obj.usuario = request.user
        
        super().save_model(request, obj, form, change)


@admin.register(CapitalGiro)
class CapitalGiroAdmin(admin.ModelAdmin):
    """
    Configuração administrativa para o modelo CapitalGiro.
    
    Exibe o histórico de movimentações do capital de giro.
    """
    
    # Campos exibidos na listagem
    list_display = [
        'data_movimentacao',
        'tipo_movimentacao',
        'valor_anterior',
        'valor_novo',
        'usuario'
    ]
    
    # Campos que podem ser usados para filtrar
    list_filter = [
        'tipo_movimentacao',
        'data_movimentacao',
        'usuario'
    ]
    
    # Campos de busca
    search_fields = [
        'descricao'
    ]
    
    # Campos somente leitura (não permite edição)
    readonly_fields = [
        'valor_anterior',
        'valor_novo',
        'tipo_movimentacao',
        'descricao',
        'usuario',
        'data_movimentacao'
    ]
    
    # Ordenação padrão (mais recentes primeiro)
    ordering = ['-data_movimentacao']
    
    # Número de itens por página
    list_per_page = 50
    
    def has_add_permission(self, request):
        """
        Desabilita a adição manual via admin.
        
        Movimentações de capital devem ser feitas através das views
        específicas para garantir a integridade dos dados.
        
        Returns:
            bool: False (não permite adicionar)
        """
        return False
    
    def has_change_permission(self, request, obj=None):
        """
        Desabilita a edição via admin.
        
        Movimentações de capital não devem ser editadas para manter
        a integridade do histórico.
        
        Returns:
            bool: False (não permite editar)
        """
        return False
    
    def has_delete_permission(self, request, obj=None):
        """
        Restringe a exclusão apenas para superusuários.
        
        Returns:
            bool: True apenas se for superusuário
        """
        return request.user.is_superuser


@admin.register(IndicadorFinanceiro)
class IndicadorFinanceiroAdmin(admin.ModelAdmin):
    """
    Configuração administrativa para o modelo IndicadorFinanceiro.
    
    Exibe os indicadores financeiros calculados por período.
    """
    
    # Campos exibidos na listagem
    list_display = [
        'periodo',
        'total_receitas',
        'total_despesas',
        'lucro_bruto',
        'margem_lucro',
        'data_atualizacao'
    ]
    
    # Campos que podem ser usados para filtrar
    list_filter = [
        'periodo'
    ]
    
    # Campos somente leitura
    readonly_fields = [
        'periodo',
        'total_receitas',
        'total_despesas',
        'lucro_bruto',
        'margem_lucro',
        'data_atualizacao'
    ]
    
    # Ordenação padrão (mais recentes primeiro)
    ordering = ['-periodo']
    
    # Número de itens por página
    list_per_page = 12  # Um ano de dados
    
    def has_add_permission(self, request):
        """
        Desabilita a adição manual via admin.
        
        Indicadores são calculados automaticamente.
        
        Returns:
            bool: False (não permite adicionar)
        """
        return False
    
    def has_change_permission(self, request, obj=None):
        """
        Desabilita a edição via admin.
        
        Indicadores são calculados automaticamente.
        
        Returns:
            bool: False (não permite editar)
        """
        return False
    
    def has_delete_permission(self, request, obj=None):
        """
        Permite exclusão apenas para superusuários.
        
        Returns:
            bool: True apenas se for superusuário
        """
        return request.user.is_superuser
