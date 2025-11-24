from django import forms
from .models import Product, Manufacturer, Category, Customer

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
            if textoBusqueda != '' and len(description) < 3:
                self.add_error('textoBusqueda', "La descripcion debe tener al menos 3 caracteres.")
            if not price is None and price <= 0:
                self.add_error('price', "El precio debe ser mayor que 0.")
                
        # Retornamos los datos limpiados
        return self.cleaned_data