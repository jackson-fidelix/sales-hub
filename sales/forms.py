from django import forms
from django.forms import inlineformset_factory
from .models import Sale, SaleItem
from products.models import Product, Supplier

# Form principal - VENDA
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['date', 'customer', 'delivery_street', 'delivery_neighborhood', 'delivery_city', 'delivery_state']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'delivery_street': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'delivery_neighborhood': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'delivery_city': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'delivery_state': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'maxlength': '2'}),
        }

# Form para CADA ITEM da venda
class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control product-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control quantity', 'min': 1}),
            'unit_price': forms.HiddenInput(),
        }

# Tabela Dinâmica com os itens
SaleItemFormSet = inlineformset_factory(
    Sale, SaleItem,
    form=SaleItemForm,
    extra=0,
    can_delete=True,
    min_num=1, # precisa ter pelo menos 1 produto
    validate_min=True
)