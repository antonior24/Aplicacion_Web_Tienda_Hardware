from django.urls import path
from . import api_views

urlpatterns = [
    path('manufacturers/', api_views.manufacturer_list, name='manufacturer_list'),
    path('orders_mejorado/', api_views.order_list_mejorado, name='order_list_mejorado'),
]
