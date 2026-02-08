from django.contrib import admin
from .models import Notificacao


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tipo', 'prioridade', 'lida', 'data_criacao')
    list_filter = ('tipo', 'prioridade', 'lida', 'data_criacao')
    search_fields = ('titulo', 'mensagem', 'usuario__username')
    readonly_fields = ('data_criacao', 'data_leitura')
    actions = ['marcar_como_lida', 'marcar_como_nao_lida']
    
    def marcar_como_lida(self, request, queryset):
        for notificacao in queryset:
            notificacao.marcar_como_lida()
        self.message_user(request, "Notificações marcadas como lidas.")
    marcar_como_lida.short_description = "Marcar como lida"
    
    def marcar_como_nao_lida(self, request, queryset):
        queryset.update(lida=False, data_leitura=None)
        self.message_user(request, "Notificações marcadas como não lidas.")
    marcar_como_nao_lida.short_description = "Marcar como não lida"
