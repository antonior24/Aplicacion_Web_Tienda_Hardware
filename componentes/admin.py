from django.contrib import admin
from .models import (
    Manufacturer, CompanyInfo, Category, Product, ProductCategory,
    Customer, Profile, Order, ShipmentDetail, OrderItem
)
# Register your models here.

admin.site.register(CompanyInfo)
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(Customer)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(ShipmentDetail)
admin.site.register(OrderItem)
admin.site.register(Manufacturer)
admin.site.register(Product)