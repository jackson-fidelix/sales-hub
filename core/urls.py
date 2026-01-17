from django.contrib import admin
from django.urls import path, include
from sales.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('vendas/', include('sales.urls')),
]
