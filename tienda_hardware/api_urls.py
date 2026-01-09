from django.urls import path
from .api_views import *

urlpatterns = [
    path('manufacturers', manufacturer_list, name='manufacturer-list'),
]