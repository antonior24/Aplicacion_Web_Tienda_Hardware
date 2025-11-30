from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('manufacturers/search/<str:texto>/', views.test_search),

    path('products/', views.product_list, name='product_list'),
    path('manufacturers/search/<str:texto>/', views.dame_fabricantes, name='dame_fabricantes'),
    
    path('manufacturers/', views.manufacturers_list, name='manufacturers_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    re_path(r'^product/sku/(?P<sku>[A-Z0-9\-]{3,30})/$', views.product_by_sku, name='product_by_sku'),
    path('products/category/<str:slug>/', views.products_by_category, name='products_by_category'),
    path('manufacturers/date/<int:year>/<int:month>/', views.manufacturers_by_year_month, name='manufacturers_by_year_month'),
    path('clientes/<int:customer_id>/pedidos/', views.pedidos_cliente, name='pedidos_cliente'),
    path('orders/last-for-product/<int:product_id>/', views.last_order_for_product, name='last_order_for_product'),
    path('products/never-ordered/', views.products_never_ordered, name='products_never_ordered'),
    path('stats/manufacturers/products-count/', views.stats_manufacturers_products, name='stats_manufacturers_products'),
    path('customers/', views.customer_list, name='customer_list'),
    path('categories/', views.category_list, name='category_list'),
    #CRUD CREATE
    path('product/create/', views.producto_create, name='producto_create'),
    path('manufacturer/create/', views.fabricante_create, name='fabricante_create'),
    path('customer/create/', views.customer_create, name='cliente_create'),
    path('category/create/', views.category_create, name='category_create'),
    path('order/create/', views.order_create, name='order_create'),
    
    #CRUD READ
    path('product/buscar/', views.producto_buscar, name='producto_buscar'),
    
    #CRUD READ avanzado
    path('product/busqueda_avanzada/', views.producto_busqueda_avanzada, name='producto_busqueda_avanzada'),
    path('manufacturer/busqueda_avanzada/', views.fabricante_busqueda_avanzada, name='fabricante_busqueda_avanzada'),
    path('customer/busqueda_avanzada/', views.cliente_busqueda_avanzada, name='cliente_busqueda_avanzada'),
    path('category/busqueda_avanzada/', views.categoria_busqueda_avanzada, name='categoria_busqueda_avanzada'),
    path('order/busqueda_avanzada/', views.pedido_busqueda_avanzada, name='pedido_busqueda_avanzada'),
    #CRUD UPDATE
    path('product/update/<int:product_id>/', views.producto_update, name='producto_update'),
    path('manufacturer/update/<int:manufacturer_id>/', views.fabricante_update, name='fabricante_update'),
    path('customer/update/<int:customer_id>/', views.cliente_update, name='cliente_update'),
    path('category/update/<int:category_id>/', views.categoria_update, name='categoria_update'),
    path('order/update/<int:order_id>/', views.pedido_update, name='pedido_update'),
    #CRUD DELETE
    path('product/delete/<int:product_id>/', views.producto_delete, name='producto_delete'),
    path('manufacturer/delete/<int:manufacturer_id>/', views.fabricante_delete, name='fabricante_delete'),
    path('customer/delete/<int:customer_id>/', views.cliente_delete, name='cliente_delete'),
    path('category/delete/<int:category_id>/', views.categoria_delete, name='categoria_delete'),
    path('order/delete/<int:order_id>/', views.pedido_delete, name='pedido_delete'),
]