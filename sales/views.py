from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Sale
from .forms import SaleForm, SaleItemFormSet
from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product
import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'base.html', {
        'title': 'Sales Hub - Portal de Vendas',
        'mensagem': 'Bem-vindo ao sistema de vendas!',
    })

class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:sale_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = SaleItemFormSet(self.request.POST)
        else:
            context['item_formset'] = SaleItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['item_formset']
        if formset.is_valid():
            sale = form.save(commit=False)
            sale.save()
            formset.instance = sale
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

def produto_api(request, pk):
    logger.info(f"Chamando API para PK: {pk}")
    try:
        product = Product.objects.get(pk=pk)
        logger.info(f"Produto encontrado: {product.id} - Nome: {product.name}")
        suppliers = list(product.suppliers.values_list('name', flat=True))
        logger.info(f"Suppliers carregados: {suppliers}")

        return JsonResponse({
            'price': str(product.price),
            'suppliers': suppliers
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)