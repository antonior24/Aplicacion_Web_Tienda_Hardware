from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

@api_view(['GET'])
def manufacturer_list(request):
    manufacturers = Manufacturer.objects.all()
    serializer = ManufacturerSerializer(manufacturers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def order_list_mejorado(request):
    orders = Order.objects.all()
    serializer = OrderSerializerMejorado(orders, many=True)
    return Response(serializer.data)