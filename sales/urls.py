from django.urls import path
from .views import SaleCreateView, api_product

app_name = 'sales'

urlpatterns = [
    path('nova/', SaleCreateView.as_view(), name='sale_create'),
    path('api/produto/<int:pk>/', api_product, name='api_product'),
]