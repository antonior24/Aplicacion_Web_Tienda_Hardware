from django.shortcuts import render
from .models import Product

# Create your views here.
def home(request):
    return render(request, 'componentes/home.html', {})

def product_list(request):
    productos = Product.objects.select_related("manufacturer").prefetch_related("categories")
    productos = productos.all()
    return render(request, 'componentes/product_list.html', {"productos_mostrar": productos})
