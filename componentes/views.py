from datetime import datetime
from itertools import count
from django.http import HttpResponse
from django.shortcuts import render
from .models import Documento, Product, Manufacturer, Category, ProductCategory, Customer, CompanyInfo, Order, OrderItem, Profile, User, Dependiente, Cliente
from django.db.models import Q, Prefetch
from django.views.defaults import page_not_found, server_error, permission_denied, bad_request
from componentes.forms import ProductoBuscarForm, ProductoForm, ManufacturerForm, CustomerForm, CategoryForm, ProductoBusquedaAvanzadaForm, OrderForm, FabricanteBusquedaAvanzadaForm, ClienteBusquedaAvanzadaForm, CategoriaBusquedaAvanzadaForm, PedidoBusquedaAvanzadaForm, ProfileForm, PerfilBusquedaAvanzadaForm, RegistroForm, DocumentoForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required

# Create your views here.

def home(request):
    
    if (not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime("%d %H:%M:%S")
    
    return render(request, 'componentes/home.html', {})

def product_list(request):
    """
    SQL (aprox):
    -- SELECT p.*, m.name AS manufacturer_name
    -- FROM componentes_product p
    -- INNER JOIN componentes_manufacturer m ON p.manufacturer_id = m.id
    -- LEFT JOIN componentes_product_categories pc ON p.id = pc.product_id
    -- LEFT JOIN componentes_category c ON pc.category_id = c.id;
    """
    productos = Product.objects.select_related("manufacturer").prefetch_related("categories")
    productos = productos.all()
    return render(request, 'componentes/product_list.html', {"productos_mostrar": productos})

def customer_list(request):
    """
    SQL (aprox):
    -- SELECT * FROM componentes_customer
    -- ORDER BY last_name ASC, first_name ASC;
    """
    clientes = Customer.objects.order_by("last_name", "first_name")
    clientes = clientes.all()
    return render(request, 'componentes/customer_list.html', {"clientes": clientes})

def category_list(request):
    """
    SQL (aprox):
    -- SELECT * FROM componentes_category
    -- ORDER BY name ASC;
    """
    categorias = Category.objects.order_by("name")
    categorias = categorias.all()
    return render(request, 'componentes/category_list.html', {"categorias": categorias})

def order_list(request):
    """
    SQL (aprox):
    -- SELECT o.*, c.first_name, c.last_name
    -- FROM componentes_order o
    -- INNER JOIN componentes_customer c ON o.customer_id = c.id
    -- ORDER BY o.created_at DESC;
    """
    ordenes = Order.objects.select_related("customer").order_by("-created_at")
    ordenes = ordenes.all()
    return render(request, 'componentes/order_list.html', {"ordenes_mostrar": ordenes})

def manufacturers_list(request):
    """
    SQL (aprox):
    -- SELECT m.*, p.id AS producto_id
    -- FROM componentes_manufacturer m
    -- LEFT JOIN componentes_product p ON p.manufacturer_id = m.id
    -- ORDER BY m.name ASC;
    """
    fabricantes = Manufacturer.objects.prefetch_related("producto_manufacturer").order_by("name")
    fabricantes = fabricantes.all()
    return render(request, 'componentes/manufacturers_list.html', {"fabricantes_mostrar": fabricantes})

def profile_list(request):
    """
    SQL (aprox):
    -- SELECT p.*, c.first_name, c.last_name
    -- FROM componentes_profile p
    -- INNER JOIN componentes_customer c ON p.customer_id = c.id;
    """
    perfiles = Profile.objects.select_related("customer").all()
    return render(request, 'componentes/profile_list.html', {"perfiles": perfiles})

def product_detail(request, product_id):
    """
    SQL (aprox):
    -- SELECT p.*, m.name AS manufacturer_name
    -- FROM componentes_product p
    -- INNER JOIN componentes_manufacturer m ON p.manufacturer_id = m.id
    -- WHERE p.id = {product_id};
    """
    producto = Product.objects.select_related("manufacturer").prefetch_related("categories").get(id=product_id)
    return render(request, 'componentes/detalles_producto.html', {"producto_mostrar": producto})

def product_by_sku(request, sku):
    """
    SQL (aprox):
    -- SELECT p.*, m.name AS manufacturer_name
    -- FROM componentes_product p
    -- INNER JOIN componentes_manufacturer m ON p.manufacturer_id = m.id
    -- WHERE p.sku = '{sku}';
    """
    producto = Product.objects.select_related("manufacturer").prefetch_related("categories").get(sku=sku)
    return render(request, 'componentes/detalles_producto.html', {"producto_mostrar": producto})

def products_by_category(request, slug):
    """
    SQL (aprox):
    -- SELECT p.*, c.slug
    -- FROM componentes_product p
    -- INNER JOIN componentes_productcategory pc ON pc.product_id = p.id
    -- INNER JOIN componentes_category c ON pc.category_id = c.id
    -- WHERE c.slug = '{slug}'
    -- ORDER BY p.price ASC;
    """
    categoria = Category.objects.get(slug=slug)
    productos = Product.objects.filter(categories=categoria).select_related("manufacturer").prefetch_related("categories").order_by("price")
    return render(request, 'componentes/product_list.html', {"productos_mostrar": productos})

def manufacturers_by_year_month(request, year, month):
    """
    SQL (aprox):
    -- SELECT * FROM componentes_manufacturer
    -- WHERE EXTRACT(YEAR FROM established) = {year}
    --   AND EXTRACT(MONTH FROM established) = {month};
    """
    fabricantes = Manufacturer.objects.filter(established__year=year, established__month=month)
    return render(request, 'componentes/manufacturers_list.html', {"fabricantes_mostrar": fabricantes})

def orders_by_customer (request, customer_id):
    """
    SQL (aprox):
    -- SELECT o.*, oi.product_id
    -- FROM componentes_order o
    -- INNER JOIN componentes_orderitem oi ON oi.order_id = o.id
    -- WHERE o.customer_id = {customer_id}
    -- ORDER BY o.created_at DESC;
    """
    ordenes = Order.objects.filter(customer__id=customer_id).prefetch_related(
        Prefetch('products')).order_by('-created_at')
    return render(request, 'componentes/orders_list.html', {"ordenes_mostrar": ordenes})

def pedidos_cliente(request, customer_id):
    """
    Muestra todos los pedidos de un cliente usando la relación inversa (Customer → Order)
    optimizada con Prefetch, como en los apuntes.
    SQL (aprox):
    -- SELECT o.*
    -- FROM componentes_order o
    -- WHERE o.customer_id = {customer_id};

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
    SQL (aprox):
    -- SELECT o.*
    -- FROM componentes_order o
    -- INNER JOIN componentes_orderitem oi ON oi.order_id = o.id
    -- WHERE oi.product_id = {product_id}
    -- ORDER BY o.created_at DESC
    -- LIMIT 1;
    """ 
    order = Order.objects.filter(items__product_id=product_id).order_by('-created_at')[0]
    return render(request, 'componentes/last_order_for_product.html', {'order': order})

def products_never_ordered(request):
    """
    SQL (aprox):
    -- SELECT p.*
    -- FROM componentes_product p
    -- LEFT JOIN componentes_orderitem oi ON oi.product_id = p.id
    -- WHERE oi.id IS NULL;
    """
    productos = Product.objects.select_related("manufacturer").prefetch_related("categories")
    productos = productos.filter(orderitem__isnull=True)
    return render(request, 'componentes/products_never_ordered.html', {"productos_no_pedidos": productos})

from django.shortcuts import render
from django.db.models import Q
from .models import Manufacturer

def dame_fabricantes(request, texto):
    """
    SQL (aprox):
    -- SELECT *
    -- FROM componentes_manufacturer
    -- WHERE active = TRUE
    --   AND (name ILIKE '%{texto}%' OR website ILIKE '%{texto}%')
    -- ORDER BY name ASC;
    """
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

def producto_create(request):
    datosproducto= None
    if request.method == 'POST':
        datosproducto = request.POST
        
    formulario_p = ProductoForm(datosproducto)
    
    if (request.method == 'POST'):
        formulario_creado = producto_crear(formulario_p)
        if (formulario_creado):
            messages.success(request, 'Producto creado correctamente.')
            return redirect('product_list')
    
    return render(request, 'componentes/crear_producto.html', {'formulario_p': formulario_p})

def producto_crear(formulario_p):
    formulario_creado = False
    if formulario_p.is_valid():
        try:
            formulario_p.save()
            formulario_creado = True
        except:
            pass
    return formulario_creado

# Fabricante Create
def fabricante_create(request):
    datosfabricante= None
    if request.method == 'POST':
        datosfabricante = request.POST
        
    formulario_f = ManufacturerForm(datosfabricante)
    
    if (request.method == 'POST'):
        formulario_creado = fabricante_crear(formulario_f)
        if (formulario_creado):
            messages.success(request, 'Fabricante creado correctamente.')
            return redirect('manufacturers_list')
    
    return render(request, 'componentes/crear_fabricante.html', {'formulario_f': formulario_f})

def fabricante_crear(formulario_f):
    formulario_creado = False
    if formulario_f.is_valid():
        try:
            formulario_f.save()
            formulario_creado = True
        except:
            pass
    return formulario_creado

# Crear Customer Create 
def customer_create(request):
    datoscustomer= None
    if request.method == 'POST':
        datoscustomer = request.POST
        
    formulario_c = CustomerForm(datoscustomer)
    
    if (request.method == 'POST'):
        formulario_creado = customer_crear(formulario_c)
        if (formulario_creado):
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('customer_list')
    
    return render(request, 'componentes/crear_cliente.html', {'formulario_c': formulario_c})

def customer_crear(formulario_c):
    formulario_creado = False
    if formulario_c.is_valid():
        try:
            formulario_c.save()
            formulario_creado = True
        except:
            pass
    return formulario_creado

def category_create(request):
    datoscategory= None
    if request.method == 'POST':
        datoscategory = request.POST
        
    formulario_cat = CategoryForm(datoscategory)
    
    if (request.method == 'POST'):
        formulario_creado = customer_crear(formulario_cat)
        if (formulario_creado):
            messages.success(request, 'Categoria creada correctamente.')
            return redirect('category_list')
    
    return render(request, 'componentes/crear_categoria.html', {'formulario_cat': formulario_cat})

def category_crear(formulario_cat):
    formulario_creado = False
    if formulario_cat.is_valid():
        try:
            formulario_cat.save()
            formulario_creado = True
        except:
            pass
    return formulario_creado

#CRUD CREATE Order
def order_create(request):
    datosorder= None
    if request.method == 'POST':
        datosorder = request.POST
        
    formulario_o = OrderForm(datosorder)
    
    if (request.method == 'POST'):
        formulario_creado = order_crear(formulario_o)
        if (formulario_creado):
            messages.success(request, 'Pedido creado correctamente.')
            return redirect('order_list')
    
    return render(request, 'componentes/crear_pedido.html', {'formulario_o': formulario_o})
def order_crear(formulario_o):
    formulario_creado = False
    if formulario_o.is_valid():
        try:
            formulario_o.save()
            formulario_creado = True
        except:
            pass
    return formulario_creado

#CRUD CREATE Profile
def profile_create(request):
    datosprofile= None
    if request.method == 'POST':
        datosprofile = request.POST
        
    formulario_p = ProfileForm(datosprofile)
    
    if (request.method == 'POST'):
        formulario_creado = profile_crear(formulario_p)
        if (formulario_creado):
            messages.success(request, 'Perfil creado correctamente.')
            return redirect('profile_list')
    
    return render(request, 'componentes/crear_perfil.html', {'formulario_p': formulario_p})

def profile_crear(formulario_p):
    formulario_creado = False
    if formulario_p.is_valid():
        try:
            formulario_p.save()
            formulario_creado = True
        except:
            pass
    return formulario_creado

#READ de productos
def producto_buscar(request):
    formulario_buscar = ProductoBuscarForm(request.GET)
    
    if formulario_buscar.is_valid():
        texto_busqueda = formulario_buscar.cleaned_data.get('textoBusqueda')
        #productos_encontrados = Product.objects.filter(
        #    Q(name__icontains=texto_busqueda) | Q(description__icontains=texto_busqueda)
        #).select_related("manufacturer").prefetch_related("categories").all()
        productos_encontrados = Product.objects.select_related("manufacturer").prefetch_related("categories")
        productos_encontrados = productos_encontrados.filter(Q(name__icontains=texto_busqueda) | Q(description__icontains=texto_busqueda)).all()
        return render(request, 'componentes/producto_busqueda.html', {
            'productos_mostrar': productos_encontrados,
            'texto_buscar': texto_busqueda
        })
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect('home')
    
#READ avanzado de productos
def producto_busqueda_avanzada(request):
    QSproductos = Product.objects.select_related("manufacturer").prefetch_related("categories")
    if (len(request.GET) > 0):
        formulario_busqueda_avanzada = ProductoBusquedaAvanzadaForm(request.GET)
        if (formulario_busqueda_avanzada.is_valid()):
            mensaje_busqueda = "Resultados de la búsqueda avanzada:\n"
            #obtenemos los filtros
            textoBusqueda = formulario_busqueda_avanzada.cleaned_data.get('textoBusqueda')
            sku = formulario_busqueda_avanzada.cleaned_data.get('sku')
            name = formulario_busqueda_avanzada.cleaned_data.get('name')
            description = formulario_busqueda_avanzada.cleaned_data.get('description')
            price = formulario_busqueda_avanzada.cleaned_data.get('price')
            stock = formulario_busqueda_avanzada.cleaned_data.get('stock')
            manufacturer = formulario_busqueda_avanzada.cleaned_data.get('manufacturer')
            categories = formulario_busqueda_avanzada.cleaned_data.get('categories')  
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if textoBusqueda != '':
                QSproductos = QSproductos.filter(
                    Q(name__icontains=textoBusqueda) | Q(description__icontains=textoBusqueda)
                )
                mensaje_busqueda += f"- Texto búsqueda: {textoBusqueda}\n"
            if sku != '':
                QSproductos = QSproductos.filter(sku__icontains=sku)
                mensaje_busqueda += f"- SKU: {sku}\n"
            if name != '':
                QSproductos = QSproductos.filter(name__icontains=name)
                mensaje_busqueda += f"- Name: {name}\n"
            if description != '':
                QSproductos = QSproductos.filter(description__icontains=description)
                mensaje_busqueda += f"- Description: {description}\n"
            if price is not None:
                QSproductos = QSproductos.filter(price=price)
                mensaje_busqueda += f"- Price: {price}\n"
            if stock is not None:
                QSproductos = QSproductos.filter(stock=stock)
                mensaje_busqueda += f"- Stock: {stock}\n"
            if manufacturer is not None:
                QSproductos = QSproductos.filter(manufacturer=manufacturer)
                mensaje_busqueda += f"- Manufacturer: {manufacturer.name}\n"
            if categories.count() > 0:
                for categoria in categories:
                    QSproductos = QSproductos.filter(categories=categoria)
                    mensaje_busqueda += f"- Category: {categoria.name}\n"
            productos_encontrados = QSproductos.all()
            
            return render(request, 'componentes/producto_busqueda.html', {
                'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
                'productos_mostrar': productos_encontrados,
                'mensaje_busqueda': mensaje_busqueda
            })
        else:
            productos_encontrados = QSproductos.all()
    else:
        productos_encontrados = QSproductos.all()
        formulario_busqueda_avanzada = ProductoBusquedaAvanzadaForm(None)
    return render(request, 'componentes/producto_busqueda_avanzada.html', {
        'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
        'productos_mostrar': productos_encontrados,
    })

#READ avanzado de fabricantes
def fabricante_busqueda_avanzada(request):
    QSfabricantes = Manufacturer.objects.all()
    if (len(request.GET) > 0):
        formulario_busqueda_avanzada = FabricanteBusquedaAvanzadaForm(request.GET)
        if (formulario_busqueda_avanzada.is_valid()):
            mensaje_busqueda = "Resultados de la búsqueda avanzada:\n"
            #obtenemos los filtros
            name = formulario_busqueda_avanzada.cleaned_data.get('name')
            website = formulario_busqueda_avanzada.cleaned_data.get('website')
            established = formulario_busqueda_avanzada.cleaned_data.get('established')
            active = formulario_busqueda_avanzada.cleaned_data.get('active')
            
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if name != '':
                QSfabricantes = QSfabricantes.filter(name__icontains=name)
                mensaje_busqueda += f"- Name: {name}\n"
            if established is not None:
                QSfabricantes = QSfabricantes.filter(established=established)
                mensaje_busqueda += f"- Established: {established}\n"
            if active is not None:
                QSfabricantes = QSfabricantes.filter(active=active)
                mensaje_busqueda += f"- Active: {active}\n"
            if website != '':
                QSfabricantes = QSfabricantes.filter(website__icontains=website)
                mensaje_busqueda += f"- Website: {website}\n"
            fabricantes_encontrados = QSfabricantes.all()
            
            return render(request, 'componentes/fabricante_busqueda.html', {
                'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
                'fabricantes_mostrar': fabricantes_encontrados,
                'mensaje_busqueda': mensaje_busqueda
            })
        else:
            fabricantes_encontrados = QSfabricantes.all()
    else:
        fabricantes_encontrados = QSfabricantes.all()
        formulario_busqueda_avanzada = FabricanteBusquedaAvanzadaForm(None)
    return render(request, 'componentes/fabricante_busqueda_avanzada.html', {
        'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
        'fabricantes_mostrar': fabricantes_encontrados,
    })

#READ avanzado de clientes
def cliente_busqueda_avanzada(request):
    QScustomers = Customer.objects.all()
    if (len(request.GET) > 0):
        formulario_busqueda_avanzada = ClienteBusquedaAvanzadaForm(request.GET)
        if (formulario_busqueda_avanzada.is_valid()):
            mensaje_busqueda = "Resultados de la búsqueda avanzada:\n"
            #obtenemos los filtros
            first_name = formulario_busqueda_avanzada.cleaned_data.get('first_name')
            last_name = formulario_busqueda_avanzada.cleaned_data.get('last_name')
            email = formulario_busqueda_avanzada.cleaned_data.get('email')
            
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if first_name != '':
                QScustomers = QScustomers.filter(first_name__icontains=first_name)
                mensaje_busqueda += f"- First Name: {first_name}\n"
            if last_name != '':
                QScustomers = QScustomers.filter(last_name__icontains=last_name)
                mensaje_busqueda += f"- Last Name: {last_name}\n"
            if email != '':
                QScustomers = QScustomers.filter(email__icontains=email)
                mensaje_busqueda += f"- Email: {email}\n"
            customers_encontrados = QScustomers.all()
            
            return render(request, 'componentes/cliente_busqueda.html', {
                'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
                'clientes': customers_encontrados,
                'mensaje_busqueda': mensaje_busqueda
            })
        else:
            customers_encontrados = QScustomers.all()
    else:
        customers_encontrados = QScustomers.all()
        formulario_busqueda_avanzada = ClienteBusquedaAvanzadaForm(None)
    return render(request, 'componentes/cliente_busqueda_avanzada.html', {
        'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
        'clientes': customers_encontrados,
    })

#READ avanzado de categorias
def categoria_busqueda_avanzada(request):
    QScategories = Category.objects.all()
    if (len(request.GET) > 0):
        formulario_busqueda_avanzada = CategoriaBusquedaAvanzadaForm(request.GET)
        if (formulario_busqueda_avanzada.is_valid()):
            mensaje_busqueda = "Resultados de la búsqueda avanzada:\n"
            #obtenemos los filtros
            name = formulario_busqueda_avanzada.cleaned_data.get('name')
            slug = formulario_busqueda_avanzada.cleaned_data.get('slug')
            description = formulario_busqueda_avanzada.cleaned_data.get('description')
            
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if name != '':
                QScategories = QScategories.filter(name__icontains=name)
                mensaje_busqueda += f"- Name: {name}\n"
            if slug != '':
                QScategories = QScategories.filter(slug__icontains=slug)
                mensaje_busqueda += f"- Slug: {slug}\n"
            if description != '':
                QScategories = QScategories.filter(description__icontains=description)
                mensaje_busqueda += f"- Description: {description}\n"
            categorias_encontradas = QScategories.all()
            
            return render(request, 'componentes/categoria_busqueda.html', {
                'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
                'categorias': categorias_encontradas,
                'mensaje_busqueda': mensaje_busqueda
            })
        else:
            categorias_encontradas = QScategories.all()
    else:
        categorias_encontradas = QScategories.all()
        formulario_busqueda_avanzada = CategoriaBusquedaAvanzadaForm(None)
    return render(request, 'componentes/categoria_busqueda_avanzada.html', {
        'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
        'categorias': categorias_encontradas,
    })
    
#CRUD READ avanzado de pedidos
def pedido_busqueda_avanzada(request):
    QSorders = Order.objects.all()
    if (len(request.GET) > 0):
        formulario_busqueda_avanzada = PedidoBusquedaAvanzadaForm(request.GET)
        if (formulario_busqueda_avanzada.is_valid()):
            mensaje_busqueda = "Resultados de la búsqueda avanzada:\n"
            #obtenemos los filtros
            customer = formulario_busqueda_avanzada.cleaned_data.get('customer')
            status = formulario_busqueda_avanzada.cleaned_data.get('status')
            total_min = formulario_busqueda_avanzada.cleaned_data.get('total_min')
            total_max = formulario_busqueda_avanzada.cleaned_data.get('total_max')
            products = formulario_busqueda_avanzada.cleaned_data.get('products')
            
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if customer is not None:
                QSorders = QSorders.filter(customer=customer)
                mensaje_busqueda += f"- Customer: {customer.first_name} {customer.last_name}\n"
            if status != '':
                QSorders = QSorders.filter(status__icontains=status)
                mensaje_busqueda += f"- Status: {status}\n"
            if total_min is not None:
                QSorders = QSorders.filter(total__gte=total_min)
                mensaje_busqueda += f"- Total mínimo: {total_min}\n"
            if total_max is not None:
                QSorders = QSorders.filter(total__lte=total_max)
                mensaje_busqueda += f"- Total máximo: {total_max}\n"
            if products.count() > 0:
                for producto in products:
                    QSorders = QSorders.filter(products=producto)
                    mensaje_busqueda += f"- Product: {producto.name}\n"
            orders_encontrados = QSorders.all()
            
            return render(request, 'componentes/pedido_busqueda.html', {
                'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
                'pedidos': orders_encontrados,
                'mensaje_busqueda': mensaje_busqueda
            })
        else:
            orders_encontrados = QSorders.all()
    else:
        orders_encontrados = QSorders.all()
        formulario_busqueda_avanzada = PedidoBusquedaAvanzadaForm(None)
    return render(request, 'componentes/pedido_busqueda_avanzada.html', {
        'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
        'pedidos': orders_encontrados,
    })
    
#Read Profile avanzado
def perfil_busqueda_avanzada(request):
    QSperfiles = Profile.objects.select_related("customer").all()
    if (len(request.GET) > 0):
        formulario_busqueda_avanzada = PerfilBusquedaAvanzadaForm(request.GET)
        if (formulario_busqueda_avanzada.is_valid()):
            mensaje_busqueda = "Resultados de la búsqueda avanzada:\n"
            #obtenemos los filtros
            customer = formulario_busqueda_avanzada.cleaned_data.get('customer')
            birth_date = formulario_busqueda_avanzada.cleaned_data.get('birthdate')
            newsletter = formulario_busqueda_avanzada.cleaned_data.get('newsletter')
            
            #Por cada filtro comprobamos si tiene un valor y lo añadimos a la QuerySet
            if customer is not None:
                QSperfiles = QSperfiles.filter(customer=customer)
                mensaje_busqueda += f"- Customer: {customer.first_name} {customer.last_name}\n"
            if birth_date is not None:
                QSperfiles = QSperfiles.filter(birthdate=birth_date)
                mensaje_busqueda += f"- Birthdate: {birth_date}\n"
            if newsletter is not None:
                QSperfiles = QSperfiles.filter(newsletter=newsletter)
                mensaje_busqueda += f"- Newsletter: {newsletter}\n"
            perfiles_encontrados = QSperfiles.all()
            
            return render(request, 'componentes/perfil_busqueda.html', {
                'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
                'perfiles': perfiles_encontrados,
                'mensaje_busqueda': mensaje_busqueda
            })
        else:
            perfiles_encontrados = QSperfiles.all()
    else:
        perfiles_encontrados = QSperfiles.all()
        formulario_busqueda_avanzada = PerfilBusquedaAvanzadaForm(None)
    return render(request, 'componentes/perfil_busqueda_avanzada.html', {
        'formulario_busqueda_avanzada': formulario_busqueda_avanzada,
        'perfiles': perfiles_encontrados,
    })

#UPDATE 
def producto_update(request, product_id):
    producto = Product.objects.get(id=product_id)
    datosproducto= None
    if request.method == 'POST':
        datosproducto = request.POST
        
    formulario_p = ProductoForm(datosproducto, instance=producto)
    
    if (request.method == 'POST'):
        if formulario_p.is_valid():
            try:
                formulario_p.save()
                messages.success(request, 'Producto actualizado correctamente.')
                return redirect('product_list')
            except Exception as e:
                pass  
    return render(request, 'componentes/actualizar_producto.html', {'formulario_p': formulario_p, 'producto': producto})

#UPDATE Fabricante
def fabricante_update(request, manufacturer_id):
    fabricante = Manufacturer.objects.get(id=manufacturer_id)
    datosfabricante= None
    if request.method == 'POST':
        datosfabricante = request.POST
        
    formulario_f = ManufacturerForm(datosfabricante, instance=fabricante)
    
    if (request.method == 'POST'):
        if formulario_f.is_valid():
            try:
                formulario_f.save()
                messages.success(request, 'Fabricante actualizado correctamente.')
                return redirect('manufacturers_list')
            except Exception as e:
                pass  
    return render(request, 'componentes/actualizar_fabricante.html', {'formulario_f': formulario_f, 'fabricante': fabricante})

#Cliente UPDATE
def cliente_update(request, customer_id):
    cliente = Customer.objects.get(id=customer_id)
    datoscustomer= None
    if request.method == 'POST':
        datoscustomer = request.POST
        
    formulario_c = CustomerForm(datoscustomer, instance=cliente)
    
    if (request.method == 'POST'):
        if formulario_c.is_valid():
            try:
                formulario_c.save()
                messages.success(request, 'Cliente actualizado correctamente.')
                return redirect('customer_list')
            except Exception as e:
                pass  
    return render(request, 'componentes/actualizar_cliente.html', {'formulario_c': formulario_c, 'cliente': cliente})

#UPDATE Categoria
def categoria_update(request, category_id):
    categoria = Category.objects.get(id=category_id)
    datoscategoria= None
    if request.method == 'POST':
        datoscategoria = request.POST
        
    formulario_cat = CategoryForm(datoscategoria, instance=categoria)
    
    if (request.method == 'POST'):
        if formulario_cat.is_valid():
            try:
                formulario_cat.save()
                messages.success(request, 'Categoria actualizada correctamente.')
                return redirect('category_list')
            except Exception as e:
                pass  
    return render(request, 'componentes/actualizar_categoria.html', {'formulario_cat': formulario_cat, 'categoria': categoria})

#UPDATE Order
def pedido_update(request, order_id):
    pedido = Order.objects.get(id=order_id)
    datospedido= None
    if request.method == 'POST':
        datospedido = request.POST
        
    formulario_o = OrderForm(datospedido, instance=pedido)
    
    if (request.method == 'POST'):
        if formulario_o.is_valid():
            try:
                formulario_o.save()
                messages.success(request, 'Pedido actualizado correctamente.')
                return redirect('home')
            except Exception as e:
                pass  
    return render(request, 'componentes/actualizar_pedido.html', {'formulario_o': formulario_o, 'pedido': pedido})

#UPDATE Profile
def perfil_update(request, profile_id):
    perfil = Profile.objects.get(id=profile_id)
    datosperfil= None
    if request.method == 'POST':
        datosperfil = request.POST
        
    formulario_p = ProfileForm(datosperfil, instance=perfil)
    
    if (request.method == 'POST'):
        if formulario_p.is_valid():
            try:
                formulario_p.save()
                messages.success(request, 'Perfil actualizado correctamente.')
                return redirect('profile_list')
            except Exception as e:
                pass  
    return render(request, 'componentes/actualizar_perfil.html', {'formulario_p': formulario_p, 'perfil': perfil})

#CRUD DELETE
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models.deletion import ProtectedError

def producto_delete(request, product_id):
    producto = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            producto.delete()
            messages.success(request, 'Producto eliminado correctamente.')
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar este producto porque está asociado a pedidos u otros registros. Por favor, elimine primero las dependencias u otro producto que no este asociado a OrderItem'
            )
        return redirect('product_list')

    return redirect('product_list')



#CRUD DELETE Fabricante
def fabricante_delete(request, manufacturer_id):
    fabricante = Manufacturer.objects.get(id=manufacturer_id)
    
    try:
        fabricante.delete()
        messages.success(request, 'Fabricante eliminado correctamente.')
        return redirect('manufacturers_list')
    except Exception as e:
        pass
    return redirect('manufacturers_list')

#CRUD DELETE Cliente
def cliente_delete(request, customer_id):
    cliente = Customer.objects.get(id=customer_id)
    
    try:
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('customer_list')
    except Exception as e:
        pass
    return redirect('customer_list')

#CRUD DELETE Categoria
def categoria_delete(request, category_id):
    categoria = Category.objects.get(id=category_id)
    
    try:
        categoria.delete()
        messages.success(request, 'Categoria eliminada correctamente.')
        return redirect('category_list')
    except Exception as e:
        pass
    return redirect('category_list')

#delete Order
def pedido_delete(request, order_id):
    pedido = Order.objects.get(id=order_id)
    
    try:
        pedido.delete()
        messages.success(request, 'Pedido eliminado correctamente.')
        return redirect('order_list')
    except Exception as e:
        pass
    return redirect('order_list')

#CRUD DELETE Profile
#@permission_required('componentes.delete_profile')
def perfil_delete(request, profile_id):
    perfil = Profile.objects.get(id=profile_id)
    
    try:
        perfil.delete()
        messages.success(request, 'Perfil eliminado correctamente.')
        return redirect('profile_list')
    except Exception as e:
        pass
    return redirect('profile_list')

#Sesiones
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            rol = int(form.cleaned_data.get('rol'))
            if (rol == User.CLIENTE):
                cliente = Cliente.objects.create(user=usuario)
                cliente.save()
            elif (rol == User.DEPENDIENTE):
                dependiente = Dependiente.objects.create(user=usuario)
                dependiente.save()
            messages.success(request, 'Usuario registrado correctamente.')
            login(request, usuario)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registration/signup.html', {'form': form})

#subidas de archivos
def subir_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento subido correctamente.')
            return redirect('lista_documentos')
    else:
        form = DocumentoForm()
    return render(request, 'componentes/subir_documento.html', {'form': form})

#lista de documentos
def lista_documentos(request):
    documentos = Documento.objects.all()
    return render(request, 'componentes/lista_documentos.html', {'documentos': documentos})

def mi_error_404(request, exception=None):
    return render(request, 'componentes/errores/404.html', None, None, 404)

def mi_error_500(request):
    return render(request, 'componentes/errores/500.html', status=500)

def mi_error_403(request, exception=None):
    return render(request, 'componentes/errores/403.html', None, None, 403)

def mi_error_400(request, exception=None):
    return render(request, 'componentes/errores/400.html', None, None, 400)
