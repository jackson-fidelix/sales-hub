from django.urls import path
from .views import SaleCreateView, produto_api

app_name = 'sales'

urlpatterns = [
    path('nova/', SaleCreateView.as_view(), name='sale_create'),
    path('api/produto/<int:pk>/', produto_api, name='produto_api'),
]