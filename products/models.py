from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    suppliers = models.ManyToManyField(Supplier, related_name='products')

    def __str__(self):
        return self.name

    def get_suppliers_display(self):
        return ", ".join(s.name for s in self.suppliers.all()) or "Nenhum fornecedor"