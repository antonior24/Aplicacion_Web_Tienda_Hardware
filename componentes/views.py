from django.shortcuts import render
from .models import Product, Manufacturer, Category, ProductCategory, Customer, CompanyInfo, Order, OrderItem
from django.db.models import Q, Prefetch

# Create your views here.
def home(request):
    return render(request, 'componentes/home.html', {})

def product_list(request):
    productos = Product.objects.select_related("manufacturer").prefetch_related("categories")
    productos = productos.all()
    return render(request, 'componentes/product_list.html', {"productos_mostrar": productos})

def manufacturers_list(request):
    fabricantes = Manufacturer.objects.prefetch_related("producto_manufacturer").order_by("name")
    fabricantes = fabricantes.all()
    return render(request, 'componentes/manufacturers_list.html', {"fabricantes_mostrar": fabricantes})

