"""
Configuração do painel de administração do Django para o módulo de Estoque.

Este arquivo personaliza a interface administrativa para os modelos
Produto e MovimentacaoEstoque, facilitando o gerenciamento via painel admin.

Autor: Manus AI
Data: 2025-12-02
"""

from django.contrib import admin
from .models import Produto, MovimentacaoEstoque


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """
    Configuração administrativa para o modelo Produto.
    
    Personaliza a exibição e funcionalidades do modelo Produto
    no painel de administração do Django.
    """
    
    # Campos exibidos na listagem
    list_display = [
        'nome',
        'preco_custo',
        'preco_venda',
        'estoque_atual',
        'estoque_minimo',
        'ativo',
        'usuario_criacao',
        'data_criacao'
    ]
    
    # Campos que podem ser usados para filtrar
    list_filter = [
        'ativo',
        'data_criacao',
        'usuario_criacao'
    ]
    
    # Campos de busca
    search_fields = [
        'nome',
        'descricao'
    ]
    
    # Campos somente leitura (não editáveis)
    readonly_fields = [
        'usuario_criacao',
        'data_criacao',
        'usuario_modificacao',
        'data_modificacao'
    ]
    
    # Organização dos campos no formulário
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'ativo')
        }),
        ('Precificação', {
            'fields': ('preco_custo', 'preco_venda')
        }),
        ('Controle de Estoque', {
            'fields': ('estoque_atual', 'estoque_minimo')
        }),
        ('Rastreamento', {
            'fields': (
                'usuario_criacao',
                'data_criacao',
                'usuario_modificacao',
                'data_modificacao'
            ),
            'classes': ('collapse',)  # Seção colapsável
        }),
    )
    
    # Ordenação padrão
    ordering = ['nome']
    
    # Número de itens por página
    list_per_page = 25
    
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


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    """
    Configuração administrativa para o modelo MovimentacaoEstoque.
    
    Personaliza a exibição das movimentações de estoque no painel admin.
    """
    
    # Campos exibidos na listagem
    list_display = [
        'produto',
        'tipo',
        'quantidade',
        'valor_unitario',
        'usuario',
        'data_movimentacao'
    ]
    
    # Campos que podem ser usados para filtrar
    list_filter = [
        'tipo',
        'data_movimentacao',
        'usuario'
    ]
    
    # Campos de busca
    search_fields = [
        'produto__nome',
        'observacao'
    ]
    
    # Campos somente leitura
    readonly_fields = [
        'usuario',
        'data_movimentacao'
    ]
    
    # Organização dos campos no formulário
    fieldsets = (
        ('Movimentação', {
            'fields': ('produto', 'tipo', 'quantidade', 'valor_unitario')
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
