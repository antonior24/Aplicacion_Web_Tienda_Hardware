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
        if ( not name is None):
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