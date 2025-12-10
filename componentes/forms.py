from django import forms
from .models import Product, Manufacturer, Category, Customer, Order, Profile, User, Documento
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta

#subida de documentos
class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['titulo', 'imagen', 'archivo']

#CRUD CREATE
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'description', 'price', 'stock', 'manufacturer', 'categories']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}), # Widget1 textarea para descripcion
            'categories': forms.CheckboxSelectMultiple(),   #Widget2 checkbox 
        }
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        stock = cleaned_data.get('stock')
        name = cleaned_data.get('name')
        
        if price <= 1:
            self.add_error('price',"El precio debe ser mayor a 1")
        if stock <= 1:
            self.add_error('stock',"El stock debe ser mayor a 1")
        if ( name is None):
            self.add_error('name',"El nombre no puede ser nulo")
        return cleaned_data

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name','website', 'established', 'active']
        widgets = {
            'website': forms.URLInput(), #Widget3 widget para url
            'established': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'), #Widget4 para fecha
        }
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        website = cleaned_data.get('website')
        established = cleaned_data.get('established')
        active = cleaned_data.get('active')
        
        if website and not (website.startswith('http://') or website.startswith('https://')):
            self.add_error('website', "La URL del sitio web debe comenzar con http:// o https://")
        if ( established is None):
            self.add_error('established',"La fecha de establecimiento no puede ser nula")
            return cleaned_data
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'wishlist']
        widgets = {
            'wishlist': forms.CheckboxSelectMultiple(), 
            'phone': forms.TextInput(attrs={'maxlength': 20}), #Widget5 widget para telefono
        }
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        wishlist = cleaned_data.get('wishlist')
        phone = cleaned_data.get('phone')
        
        # comprobar que haya al menos un elemento seleccionado en wishlist
        if not wishlist or wishlist.count() == 0:
            self.add_error('wishlist', "Debe seleccionar al menos un producto en la lista de deseos.")
        if (len(phone) < 7):
            self.add_error('phone', "El teléfono debe tener al menos 7 dígitos")
        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'parent']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'name': forms.TextInput(attrs={'maxlength': 60}),
            'parent': forms.Select() #Widget6 widget para seleccionar parent
        }
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        slug = cleaned_data.get('slug')
        
        # Nombre y descripción no pueden ser iguales
        #El slug no puede ser mayor que el nombre
        if name == slug:
            self.add_error('slug', "El slug no puede ser igual al nombre.")
        if len(slug) > len(name):
            self.add_error('slug', "El slug no puede ser más largo que el nombre.")
        return cleaned_data

#quinto CREATE
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'total', 'products']
        widgets = {
            'products': forms.CheckboxSelectMultiple(),
            'total': forms.NumberInput(attrs={'step': '0.01'}),  #Widget7 para decimales
        }
    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        total = cleaned_data.get('total')
        if total < 0:
            self.add_error('total', "El total no puede ser negativo.")
        if customer is None:
            self.add_error('customer', "El cliente es obligatorio.")
        return cleaned_data
        
#Sexto CREATE
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['customer', 'birth_date', 'newsletter', 'notes']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'notes': forms.PasswordInput(render_value=True), #Widget8 widget para notas como contraseña
            'newsletter': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}) #Widget9 widget para newsletter
        }
    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        birth_date = cleaned_data.get('birth_date')
        # la fecha de nacimiento debe tener minimo 18 años
        #if birth_date and birth_date > forms.fields.datetime.date.today():
        #    self.add_error('birth_date', "La fecha de nacimiento no puede ser en el futuro.")
        if birth_date:
            today = date.today()
            age_limit = today - timedelta(days=18*365.25)  # Aproximadamente 18 años
            if birth_date > age_limit:
                self.add_error('birth_date', "El cliente debe tener al menos 18 años.")
        if customer is None:
            self.add_error('customer', "El cliente es obligatorio.")
        return cleaned_data
#READ
class ProductoBuscarForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
# READ avanzado
class ProductoBusquedaAvanzadaForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    sku = forms.CharField(required=False)
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    price = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    stock = forms.IntegerField(required=False)
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), required=False)
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    
    def clean(self):
        super().clean()
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        sku = self.cleaned_data.get('sku')
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        price = self.cleaned_data.get('price')
        stock = self.cleaned_data.get('stock')
        manufacturer = self.cleaned_data.get('manufacturer')
        categories = self.cleaned_data.get('categories')  
        
        # Controlamos los campos
        if (textoBusqueda == '' 
            and (sku == '')
            and (name == '')
            and (description == '')
            and (price is None)
            and (stock is None)
            and (manufacturer is None)
            and (categories.count() == 0)
        ):
            self.add_error('textoBusqueda', "Debe rellenar al menos un campo para la búsqueda avanzada.")
            self.add_error('sku', "")
            self.add_error('name', "")
            self.add_error('description', "")
            self.add_error('price', "")
            self.add_error('stock', "")
            self.add_error('manufacturer', "")
            self.add_error('categories', "")
        else:
            #if textoBusqueda != '' and len(description) < 3:
             #   self.add_error('textoBusqueda', "La descripcion debe tener al menos 3 caracteres.")
            if not price is None and price <= 1:
                self.add_error('price', "El precio debe ser mayor que 0.")
            #stock debe ser positivo
            if not stock is None and stock < 0:
                self.add_error('stock', "El stock no puede ser negativo.")
                
        # Retornamos los datos limpiados
        return self.cleaned_data

# READ avanzado de fabricantes
class FabricanteBusquedaAvanzadaForm(forms.Form):
    name = forms.CharField(required=False)
    established = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    active = forms.NullBooleanField(required=False, widget=forms.Select(choices=[('', '---------'), ('True', 'Sí'), ('False', 'No')]))
    website = forms.URLField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        website = cleaned_data.get('website')
        established = cleaned_data.get('established')
        active = cleaned_data.get('active')
        
        if (name == '' 
            and established is None
            and active is None):
            self.add_error('name', "Debe rellenar al menos un campo para la búsqueda avanzada.")
            self.add_error('established', "")
            self.add_error('active', "")
            self.add_error('website', "")
        else:
            if name and len(name) < 3:
                self.add_error('name', "El nombre debe tener al menos 3 caracteres.")
            # la fecha de establecimiento no puede ser en el futuro
            if established and established > forms.fields.datetime.date.today():
                self.add_error('established', "La fecha de establecimiento no puede ser en el futuro.")
        
        return cleaned_data
# READ avanzado de clientes
class ClienteBusquedaAvanzadaForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        
        if (first_name == '' 
            and last_name == ''
            and email == ''
            and phone == ''):
            self.add_error('first_name', "Debe rellenar al menos un campo para la búsqueda avanzada.")
            self.add_error('last_name', "")
            self.add_error('email', "")
            self.add_error('phone', "")
        else:
            if first_name and len(first_name) < 2:
                self.add_error('first_name', "El nombre debe tener al menos 2 caracteres.")
            # el email debe contener '@'
            if email and 'gmail' not in email:
                self.add_error('email', "El email debe ser un gmail(hotmail, outlook, etc no válidos).")
        
        return cleaned_data
    
#READ avanzado de categorias
class CategoriaBusquedaAvanzadaForm(forms.Form):
    name = forms.CharField(required=False)
    slug = forms.CharField(required=False)
    description = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        slug = cleaned_data.get('slug')
        description = cleaned_data.get('description')
        
        if (name == '' 
            and slug == ''
            and description == ''):
            self.add_error('name', "Debe rellenar al menos un campo para la búsqueda avanzada.")
            self.add_error('slug', "")
            self.add_error('description', "")
        else:
            if name and len(name) < 3:
                self.add_error('name', "El nombre debe tener al menos 3 caracteres.")
            #la descripcion no puede ser igual al nombre
            if description and name and description == name:
                self.add_error('description', "La descripción no puede ser igual al nombre.")
        
        return cleaned_data

#Busqueda avanzada de pedidos
class PedidoBusquedaAvanzadaForm(forms.Form):
    #si estoy logueado como cliente, no muestro el campo customer
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False)
    status = forms.ChoiceField(choices=[('', '---------')] + list(Order.STATUS_CHOICES), required=False)
    total_min = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    total_max = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 🟦 Si el usuario está logueado como cliente → ocultamos el campo como hidden
        if user and user.is_authenticated and user.rol == User.CLIENTE:
            customer_qs = Customer.objects.filter(user=user)
            if customer_qs.exists():
                self.fields["customer"].queryset = customer_qs
                self.fields["customer"].initial = customer_qs.first()
            self.fields["customer"].widget = forms.HiddenInput()
    
    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        status = cleaned_data.get('status')
        total_min = cleaned_data.get('total_min')
        total_max = cleaned_data.get('total_max')
        products = cleaned_data.get('products')
        
        if (customer is None
            and status == ''
            and total_min is None
            and total_max is None
            and products.count() == 0):
            self.add_error('customer', "Debe rellenar al menos un campo para la búsqueda avanzada.")
            self.add_error('status', "")
            self.add_error('total_min', "")
            self.add_error('total_max', "")
            self.add_error('products', "")
        else:
            # productos no puede estar vacío
            if products.count() == 0:
                self.add_error('products', "Debe seleccionar al menos un producto.")
            #el total maximo debe ser mayor que el minimo
            if not total_min is None and total_min < 0:
                self.add_error('total_min', "El total mínimo no puede ser negativo.")
            if not total_max is None and total_max < 0:
                self.add_error('total_max', "El total máximo no puede ser negativo.")
            if not total_min is None and not total_max is None and total_max < total_min:
                self.add_error('total_max', "El total máximo debe ser mayor o igual al total mínimo.")
        
        return cleaned_data
    
#Busqueda avancada de perfiles
class PerfilBusquedaAvanzadaForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    newsletter = forms.NullBooleanField(required=False, widget=forms.Select(choices=[('', '---------'), ('True', 'Sí'), ('False', 'No')]))
    
    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        birth_date = cleaned_data.get('birth_date')
        newsletter = cleaned_data.get('newsletter')
        
        if (customer is None
            and birth_date is None
            and newsletter is None):
            self.add_error('customer', "Debe rellenar al menos un campo para la búsqueda avanzada.")
            self.add_error('birth_date', "")
            self.add_error('newsletter', "")
        else:
            if birth_date and birth_date > forms.fields.datetime.date.today():
                self.add_error('birth_date', "La fecha de nacimiento no puede ser en el futuro.")
            #no puede tener mas de 120 años
            if birth_date:
                today = date.today()
                age_limit = today - timedelta(days=120*365.25)  # Aproximadamente 120 años
                if birth_date < age_limit:
                    self.add_error('birth_date', "La fecha de nacimiento no puede indicar más de 120 años.")
        
        return cleaned_data

#Formulario de registro de usuario
class RegistroForm(UserCreationForm):
    roles = (
            (User.CLIENTE, 'Cliente'),
            (User.DEPENDIENTE, 'Dependiente'),
    )
    rol = forms.ChoiceField(choices=roles)
    class Meta:
        model = User
        fields = ['username', 'email', 'rol', 'password1', 'password2', 'rol']

#class PrestamoFormGenericoRequest(forms.Form):
    
    #def __init__(self, *args, **kwargs):
     #   self.request = kwargs.pop("request")
      #  super(PrestamoFormGenericoRequest, self).__init__(*args, **kwargs)
       # librosdisponibles = Libro.objects.exclude(prestamo__cliente=self.request.user.cliente).all()
        #self.fields["libro"] = forms.ModelChoiceField(
         #   queryset=librosdisponibles,
          #  widget=forms.Select,
           # required=True,
            #empty_label="Ninguna"
        #)
        
class OrderFormRequest(OrderForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(OrderFormRequest, self).__init__(*args, **kwargs)
        # Filtrar los productos disponibles para el usuario actual
        productos_disponibles = Product.objects.exclude(orders__customer__user=self.request.user).all()
        self.fields["products"] = forms.ModelMultipleChoiceField(
            queryset=productos_disponibles,
            widget=forms.CheckboxSelectMultiple,
            required=True,
        )
        #  Controlar el campo 'customer' según el rol CONSULTAR CON EL PROFESOR
        if self.request.user.is_authenticated:
            usuario = self.request.user

            # Si es CLIENTE: fijamos su Customer y ocultamos el campo
            if usuario.rol == User.CLIENTE:
                customer_qs = Customer.objects.filter(user=usuario)
                if customer_qs.exists():
                    self.fields["customer"].queryset = customer_qs
                    self.fields["customer"].initial = customer_qs.first()
                self.fields["customer"].widget = forms.HiddenInput()

            # Si es DEPENDIENTE: dejamos el select normal (puede elegir cualquier cliente)
            elif usuario.rol == User.DEPENDIENTE:
                self.fields["customer"].queryset = Customer.objects.all()