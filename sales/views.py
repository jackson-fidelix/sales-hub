from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Sale
from .forms import SaleForm, SaleItemFormSet, SaleItem, SaleItemForm, inlineformset_factory
from django.shortcuts import render, redirect
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
            context['item_formset'] = SaleItemFormSet(self.request.POST, prefix='items')
        else:
            context['item_formset'] = SaleItemFormSet(prefix='items')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['item_formset']

        print("FORM VALID:", form.is_valid())
        print("FORM ERRORS:", form.errors)
        print("FORMSET VALID:", formset.is_valid())
        print("FORMSET ERRORS:", formset.errors)

        if not formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form))

        # Savando a venda
        sale = form.save(commit=False)
        sale.created_by = self.request.user
        sale.save()

        # Salvando os itens da venda
        formset.instance = sale
        items = formset.save(commit=False)

        for item in items:
            if not item.product or not item.quantity:
                continue
            
            item.sale = sale
            item.unit_price = item.product.price
            item.save()

        return redirect(self.success_url)



def api_product(request, pk):
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
    
