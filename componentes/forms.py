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