from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('manufacturers/', views.manufacturers_list, name='manufacturers_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    re_path(r'^product/sku/(?P<sku>[A-Z0-9\-]{3,30})/$', views.product_by_sku, name='product_by_sku'),
    path('products/category/<str:slug>/', views.products_by_category, name='products_by_category'),
    path('manufacturers/date/<int:year>/<int:month>/', views.manufacturers_by_year_month, name='manufacturers_by_year_month'),
    path('clientes/<int:customer_id>/pedidos/', views.pedidos_cliente, name='pedidos_cliente'),
    path('orders/last-for-product/<int:product_id>/', views.last_order_for_product, name='last_order_for_product'),

]