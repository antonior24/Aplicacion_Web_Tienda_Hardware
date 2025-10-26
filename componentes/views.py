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

def product_detail(request, product_id):
    producto = Product.objects.select_related("manufacturer").prefetch_related("categories").get(id=product_id)
    return render(request, 'componentes/detalles_producto.html', {"producto_mostrar": producto})

def product_by_sku(request, sku):
    producto = Product.objects.select_related("manufacturer").prefetch_related("categories").get(sku=sku)
    return render(request, 'componentes/detalles_producto.html', {"producto_mostrar": producto})

def products_by_category(request, slug):
    categoria = Category.objects.get(slug=slug)
    productos = Product.objects.filter(categories=categoria).select_related("manufacturer").prefetch_related("categories").order_by("price")
    return render(request, 'componentes/product_list.html', {"productos_mostrar": productos})

def manufacturers_by_year_month(request, year, month):
    fabricantes = Manufacturer.objects.filter(established__year=year, established__month=month)
    return render(request, 'componentes/manufacturers_list.html', {"fabricantes_mostrar": fabricantes})