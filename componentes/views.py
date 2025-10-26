from itertools import count
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, Manufacturer, Category, ProductCategory, Customer, CompanyInfo, Order, OrderItem
from django.db.models import Q, Prefetch
from django.views.defaults import page_not_found, server_error, permission_denied, bad_request

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

def orders_by_customer (request, customer_id):
    ordenes = Order.objects.filter(customer__id=customer_id).prefetch_related(
        Prefetch('products')).order_by('-created_at')
    return render(request, 'componentes/orders_list.html', {"ordenes_mostrar": ordenes})

def pedidos_cliente(request, customer_id):
    """
    Muestra todos los pedidos de un cliente usando la relación inversa (Customer → Order)
    optimizada con Prefetch, como en los apuntes.
    """
    cliente = Customer.objects.prefetch_related(Prefetch("orders")).get(id=customer_id)
    pedidos = cliente.orders.all()   # relación inversa optimizada
    return render(request, 'componentes/pedidos_cliente.html', {
        'cliente': cliente,
        'pedidos': pedidos
    })
    
def last_order_for_product(request, product_id):
    """
    Muestra el último pedido que contiene un producto concreto.
    """ 
    order = Order.objects.filter(items__product_id=product_id).order_by('-created_at')[0]
    return render(request, 'componentes/last_order_for_product.html', {'order': order})

def products_never_ordered(request):
    productos = Product.objects.select_related("manufacturer").prefetch_related("categories")
    productos = productos.filter(orderitem__isnull=True)
    return render(request, 'componentes/products_never_ordered.html', {"productos_no_pedidos": productos})

from django.shortcuts import render
from django.db.models import Q
from .models import Manufacturer

def dame_fabricantes(request, texto):
    print("Texto recibido:", texto)  # Debug

    fabricantes = Manufacturer.objects.filter(
        (Q(name__icontains=texto) | Q(website__icontains=texto)) & Q(active=True)
    ).order_by("name")

    print("Fabricantes encontrados:", list(fabricantes))  # Debug

    return render(request, "componentes/manufacturers_list.html", {"fabricantes_mostrar": fabricantes})


def test_search(request, texto):
    print("=== TEST VIEW EJECUTADA ===")
    print("Texto recibido:", texto)
    return HttpResponse(f"Has buscado: {texto}")

def stats_manufacturers_products(request):
    """
    Vista: Muestra estadísticas de los fabricantes (Manufacturer) con el número de productos asociados.
    SQL (aprox):
    -- SELECT m.id, m.name, COUNT(p.id) AS productos_total
    -- FROM manufacturer m
    -- LEFT JOIN product p ON p.manufacturer_id = m.id
    -- GROUP BY m.id
    -- ORDER BY productos_total DESC;
    """
    fabricantes = (
        Manufacturer.objects
        .annotate(total_productos=count('producto_manufacturer'))
        .order_by('-total_productos')
    )

    return render(
        request,
        'componentes/stats_manufacturers_products.html',
        {'fabricantes': fabricantes}
    )
    
def mi_error_404(request, exception=None):
    return render(request, 'componentes/errores/404.html', None, None, 404)

def mi_error_500(request):
    return render(request, 'componentes/errores/500.html', status=500)

def mi_error_403(request, exception=None):
    return render(request, 'componentes/errores/403.html', None, None, 403)

def mi_error_400(request, exception=None):
    return render(request, 'componentes/errores/400.html', None, None, 400)
