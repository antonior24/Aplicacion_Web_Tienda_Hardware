# catalogo/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
#importar para las sesiones
from django.contrib.auth.models import AbstractUser

#documento
from django.db import models

class Documento(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    archivo = models.FileField(upload_to='archivos/', blank=True, null=True)

    def __str__(self):
        return self.titulo


#Usuarios
class User(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    DEPENDIENTE = 3
    
    ROLES = (
        (ADMINISTRADOR, 'Administrador'),
        (CLIENTE, 'Cliente'),
        (DEPENDIENTE, 'Dependiente'),
    )
    
    rol = models.PositiveSmallIntegerField(choices=ROLES, default=1)
    
class Dependiente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

# 1) Manufacturer
class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Nombre del fabricante")
    website = models.URLField(blank=True, null=True)
    established = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# 2) CompanyInfo (OneToOne con Manufacturer)
class CompanyInfo(models.Model):
    manufacturer = models.OneToOneField(Manufacturer, on_delete=models.CASCADE, related_name='company_info')
    vat_number = models.CharField(max_length=50, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Info {self.manufacturer.name}"

# 3) Category (ManyToOne a sí misma como parent)
class Category(models.Model):
    name = models.CharField(max_length=60, db_index=True)
    slug = models.SlugField(max_length=70, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')

    def __str__(self):
        return self.name

# 4) Product
class Product(models.Model):
    sku = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, related_name='producto_manufacturer')
    categories = models.ManyToManyField(Category, through='ProductCategory', related_name='producto_categories')

    def __str__(self):
        return f"{self.sku} - {self.name}"

# 5) ProductCategory (tabla intermedia ManyToMany con atributos extras)
class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('product', 'category')

# 6) Customer
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    wishlist = models.ManyToManyField(Product, blank=True, related_name='wishlisted_by')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 7) Profile (OneToOne con Customer)
class Profile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    newsletter = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

# 8) Order
class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('X', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
    
    # NUEVO: usuario que crea el pedido
    #En los formularios de crear debe incluirse siempre el usuario 
    # que crea dicho registro por la sesión del usuario. 
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='created_orders')

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

# 9) ShipmentDetail (OneToOne con Order)
class ShipmentDetail(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipment')
    tracking_code = models.CharField(max_length=120, blank=True)
    shipped_date = models.DateField(null=True, blank=True)
    delivery_estimate = models.DateField(null=True, blank=True)

# 10) OrderItem (tabla intermedia entre Order y Product con atributos extras)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        unique_together = ('order', 'product')

    def line_total(self):
        return self.quantity * self.unit_price