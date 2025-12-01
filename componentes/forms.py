from django import forms
from .models import Product, Manufacturer, Category, Customer, Order, Profile

#CRUD CREATE
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'description', 'price', 'stock', 'manufacturer', 'categories']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'categories': forms.CheckboxSelectMultiple(),
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
            'website': forms.URLInput(),
            'established': forms.DateInput(attrs={'type': 'date'}),
        }
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'wishlist']
        widgets = {
            'wishlist': forms.CheckboxSelectMultiple(), 
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'parent']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

#quinto CREATE
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'total', 'products']
        widgets = {
            'products': forms.CheckboxSelectMultiple(),
            'total': forms.NumberInput(attrs={'step': '0.01'}),  # Para decimales
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
            'notes': forms.Textarea(attrs={'rows': 3}), 
        }
        def clean(self):
            cleaned_data = super().clean()
            customer = cleaned_data.get('customer')
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
            if not price is None and price <= 0:
                self.add_error('price', "El precio debe ser mayor que 0.")
                
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
            
            if website and not (website.startswith('http://') or website.startswith('https://')):
                self.add_error('website', "La URL del sitio web debe comenzar con http:// o https://")
        
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
            if last_name and len(last_name) < 2:
                self.add_error('last_name', "El apellido debe tener al menos 2 caracteres.")
        
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
            if slug and len(slug) < 3:
                self.add_error('slug', "El slug debe tener al menos 3 caracteres.")
        
        return cleaned_data

#Busqueda avanzada de pedidos
class PedidoBusquedaAvanzadaForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False)
    status = forms.ChoiceField(choices=[('', '---------')] + list(Order.STATUS_CHOICES), required=False)
    total = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    
    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        status = cleaned_data.get('status')
        total = cleaned_data.get('total')
        products = cleaned_data.get('products')
        
        if (customer is None
            and status == ''
            and total is None
            and products.count() == 0):
            self.add_error('customer', "Debe rellenar al menos un campo para la búsqueda avanzada.")
            self.add_error('status', "")
            self.add_error('total_min', "")
            self.add_error('total_max', "")
            self.add_error('products', "")
        else:
            if not total is None and total < 0:
                self.add_error('total', "El total no puede ser negativo.")
        
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
        
        return cleaned_data