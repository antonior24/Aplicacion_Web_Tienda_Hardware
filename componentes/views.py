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
