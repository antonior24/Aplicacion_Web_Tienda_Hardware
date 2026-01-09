from rest_framework import serializers
from .models import *

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializerMejorado(serializers.ModelSerializer):
    customer = CustomerSerializer()
    #many to many
    products = ProductSerializer( read_only=True , many=True)
    #dar formato a la fecha
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # Para obtener el valor del choice
    status = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'