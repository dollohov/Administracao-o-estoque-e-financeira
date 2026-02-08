"""
Configuracao do Django Admin para o app de Auditoria.
"""

from django.contrib import admin
from .models import LogAuditoria, LogAcessoDadosSensiveis, SolicitacaoLGPD


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    """Admin para logs de auditoria."""
    
    list_display = ['usuario', 'tipo_acao', 'content_type', 'object_id', 'data_hora']
    list_filter = ['tipo_acao', 'data_hora', 'usuario']
    search_fields = ['usuario__username', 'descricao', 'endereco_ip']
    readonly_fields = ['usuario', 'tipo_acao', 'content_type', 'object_id', 
                       'valores_anteriores', 'valores_novos', 'descricao', 
                       'endereco_ip', 'user_agent', 'data_hora']
    
    def has_add_permission(self, request):
        """Impedir adicao manual de logs."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Impedir delecao de logs."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Impedir edicao de logs."""
        return False


@admin.register(LogAcessoDadosSensiveis)
class LogAcessoDadosSensiveisAdmin(admin.ModelAdmin):
    """Admin para logs de acesso a dados sensiveis."""
    
    list_display = ['usuario', 'tipo_dado', 'cliente_nome', 'data_hora']
    list_filter = ['tipo_dado', 'data_hora', 'usuario']
    search_fields = ['usuario__username', 'cliente_nome', 'endereco_ip']
    readonly_fields = ['usuario', 'tipo_dado', 'cliente_id', 'cliente_nome',
                       'motivo', 'endereco_ip', 'user_agent', 'data_hora']
    
    def has_add_permission(self, request):
        """Impedir adicao manual de logs."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Impedir delecao de logs."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Impedir edicao de logs."""
        return False


@admin.register(SolicitacaoLGPD)
class SolicitacaoLGPDAdmin(admin.ModelAdmin):
    """Admin para solicitacoes LGPD."""
    
    list_display = ['cliente_nome', 'tipo_solicitacao', 'status', 'data_solicitacao']
    list_filter = ['tipo_solicitacao', 'status', 'data_solicitacao']
    search_fields = ['cliente_nome', 'cliente_id', 'descricao']
    readonly_fields = ['data_solicitacao']
    
    fieldsets = (
        ('Informacoes da Solicitacao', {
            'fields': ('cliente_id', 'cliente_nome', 'tipo_solicitacao', 'descricao', 'data_solicitacao')
        }),
        ('Processamento', {
            'fields': ('status', 'usuario_responsavel', 'data_conclusao', 'resposta')
        }),
    )
    
    actions = ['marcar_concluida', 'marcar_recusada']
    
    def marcar_concluida(self, request, queryset):
        """Acao para marcar solicitacoes como concluidas."""
        for solicitacao in queryset:
            solicitacao.marcar_concluida(request.user)
        self.message_user(request, f'{queryset.count()} solicitacao(oes) marcada(s) como concluida(s).')
    
    marcar_concluida.short_description = 'Marcar como Concluida'
    
    def marcar_recusada(self, request, queryset):
        """Acao para marcar solicitacoes como recusadas."""
        for solicitacao in queryset:
            solicitacao.marcar_recusada(request.user, 'Recusada pelo administrador')
        self.message_user(request, f'{queryset.count()} solicitacao(oes) marcada(s) como recusada(s).')
    
    marcar_recusada.short_description = 'Marcar como Recusada'
