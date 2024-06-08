from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from .models import Engine, Car, CarUser
from .serializers import Car_CarUserWritableNestedSerializer, CarUser_CarNested_Serializer, CarUser_WritableNestedSerializer, EngineSerializer, CarSerializer, CarUserSerializer
from .filters import EngineFilter, CarFilter

class EngineViewSet(viewsets.ModelViewSet):
    serializer_class = EngineSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = EngineFilter
    queryset = Engine.objects.all()
    

class CarViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CarFilter
    queryset = Car.objects.all()


    def create(self, request, *args, **kwargs):
        """
        Test with POSTMAN

        curl --location 'http://127.0.0.1:8000/motorizations/api/cars/' \
--header 'Authorization: Token be4126fdd668feda4c4a4c9b7761d5af15c1dee3' \
--header 'Content-Type: application/json' \
--data '{
    "name": "advanced-electric",
    "engine": "1",
    "car_user": [
        {
            "user": 1,
            "number_plate": "admin123"
        },
        {
            "user": 1,
            "number_plate": "admin456"
        }
    ]
}'
        """
        return super().create(request, *args, **kwargs)
    
    def get_serializer_class(self):
        return CarSerializer
        #return Car_CarUserWritableNestedSerializer
      
    
class CarUserViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = '__all__'
    queryset = CarUser.objects.all()
    
    def get_serializer_class(self):
        car = self.request.data.get('car')
        if car and isinstance(car, dict):
            return CarUser_CarNested_Serializer
            #return CarUser_WritableNestedSerializer
        return CarUserSerializer
    
    
    def create(self, request, *args, **kwargs):
        """
        Test with POSTMAN

        curl --location 'http://127.0.0.1:8000/motorizations/api/cars-users/' \
--header 'Authorization: Token be4126fdd668feda4c4a4c9b7761d5af15c1dee3' \
--header 'Content-Type: application/json' \
--data '{
    "car": {
            "name": "advanced-electric",
            "engine": "1"
        },
    "user" : 1,
    "number_plate" : "admin"
}'
        """
        return super().create(request, *args, **kwargs)