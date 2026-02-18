from django.contrib import admin

class TenantAdmin(admin.ModelAdmin):
    """
    Mixin para garantir que o Admin do Django respeite o isolamento por empresa (Tenant).
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company=request.company)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.company = request.company
        super().save_model(request, obj, form, change)

