from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    delivery_street = models.CharField(max_length=200)
    delivery_neighborhood = models.CharField(max_length=100)
    delivery_city = models.CharField(max_length=100)
    delivery_state = models.CharField(max_length=2)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venda #{self.pk} - {self.customer} - {self.date}"

    def get_total(self):
        return sum(item.subtotal() for item in self.items.all()) or 0

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"