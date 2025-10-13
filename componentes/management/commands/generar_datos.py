from django.core.management.base import BaseCommand
from faker import Faker
import random

from componentes.models import (
    Manufacturer, CompanyInfo, Category, Product, ProductCategory,
    Customer, Profile, Order, ShipmentDetail, OrderItem
)

class Command(BaseCommand):
    help = "Genera datos falsos con Faker para todos los modelos"

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        
        for _ in range(10):
            Customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number()
            )


        self.stdout.write(self.style.SUCCESS("✅ Datos generados correctamente"))
