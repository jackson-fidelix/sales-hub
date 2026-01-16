from django.contrib import admin
from .models import Supplier, Product

@admin.register(Supplier)
class SuplierAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_suppliers_display')
    list_filter = ('suppliers',)
    search_fields = ('name',)