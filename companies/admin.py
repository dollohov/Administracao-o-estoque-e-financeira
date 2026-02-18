from django.contrib import admin
from .models import Company, UserCompany

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'plano', 'active', 'created_at')
    list_filter = ('plano', 'active', 'created_at')
    search_fields = ('name', 'cnpj')
    ordering = ('name',)

@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'role')
    list_filter = ('company', 'role')
    search_fields = ('user__username', 'company__name')
