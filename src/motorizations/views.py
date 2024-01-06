from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import Car_user_Write_Permission
from .models import Engine, Car, Car_user
from .serializers import Engine_Serializer, Car_Serializer, Car_user_Serializer
from .filters import Engine_Filter, Car_Filter


class Engine_ViewSet(viewsets.ModelViewSet):
    serializer_class = Engine_Serializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = Engine_Filter
    queryset = Engine.objects.all()
    

class Car_ViewSet(viewsets.ModelViewSet):
    serializer_class = Car_Serializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = Car_Filter
    queryset = Car.objects.all()
    
    
class Car_user_ViewSet(viewsets.ModelViewSet):
    serializer_class = Car_user_Serializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = '__all__'
    queryset = Car_user.objects.all()

    def get_permissions(self):
        i = super().get_permissions()
        i.append(Car_user_Write_Permission())
        return i