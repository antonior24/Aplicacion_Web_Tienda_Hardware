from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('manufacturers/', views.manufacturers_list, name='manufacturers_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    re_path(r'^product/sku/(?P<sku>[A-Z0-9\-]{3,30})/$', views.product_by_sku, name='product_by_sku'),
]