from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    raw_id_fields = ["produto"]

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "cliente",
        "vendedor",
        "data_pedido",
        "status",
        "valor_total",
    )
    list_filter = ("status", "data_pedido", "vendedor", "cliente")
    search_fields = (
        "pk__iexact",
        "cliente__nome_completo__icontains",
        "vendedor__username__icontains",
    )
    raw_id_fields = ["cliente", "vendedor"]
    inlines = [ItemPedidoInline]
    date_hierarchy = "data_pedido"
    actions = ["aprovar_pedidos", "cancelar_pedidos"]

    def aprovar_pedidos(self, request, queryset):
        queryset.update(status="APROVADO")
        self.message_user(request, "Pedidos selecionados foram aprovados com sucesso.")
    aprovar_pedidos.short_description = "Aprovar pedidos selecionados"

    def cancelar_pedidos(self, request, queryset):
        queryset.update(status="CANCELADO")
        self.message_user(request, "Pedidos selecionados foram cancelados com sucesso.")
    cancelar_pedidos.short_description = "Cancelar pedidos selecionados"

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "produto", "quantidade", "preco_unitario", "desconto", "calcular_subtotal")
    list_filter = ("produto", "pedido__status")
    search_fields = (
        "pedido__pk__iexact",
        "produto__nome__icontains",
    )
    raw_id_fields = ["pedido", "produto"]
