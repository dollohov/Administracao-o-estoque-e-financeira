from django.contrib import admin
from .models import Cliente, ContatoCliente
from base.admin import TenantAdmin

class ContatoClienteInline(admin.TabularInline):
    model = ContatoCliente
    extra = 1

@admin.register(Cliente)
class ClienteAdmin(TenantAdmin):
    list_display = ('nome', 'email', 'cpf_cnpj', 'cidade', 'estado', 'ativo')
    list_filter = ('ativo', 'estado', 'anonimizado')
    search_fields = ('nome', 'email', 'cpf_cnpj')
    inlines = [ContatoClienteInline]
    readonly_fields = ('data_criacao', 'data_modificacao', 'usuario_criacao', 'usuario_modificacao')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario_criacao = request.user
        obj.usuario_modificacao = request.user
        super().save_model(request, obj, form, change)
