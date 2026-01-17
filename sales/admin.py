from django.contrib import admin
from .models import Customer, Sale, SaleItem
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'customer', 'products','get_total')
    list_filter = ('date', 'customer')
    search_fields = ('customer__name',)
    date_hierarchy = 'date'

    def products(self, obj):
        return ", ".join(
            f"{item.product.name} ({item.quantity} x R$ {item.unit_price})"
            for item in obj.items.all()
        )

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'subtotal')