from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from .models import Engine, Car, CarUser
from .serializers import (Car__CarUser__Engine_WritableNestedSerializer, 
                          Car__CarUser_WritableNestedSerializer, 
                          Car__Engine_WritableNestedSerializer, 
                          CarUser__Car__Engine_WritableNestedSerializer, 
                          CarUser__Car_WritableNestedSerializer, 
                          CarUserValidateModelSerializer, 
                          EngineSerializer, 
                          CarSerializer, 
                        )
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

        curl --location --request PUT 'http://127.0.0.1:8000/motorizations/api/cars/130/' \
--header 'Authorization: Token be4126fdd668feda4c4a4c9b7761d5af15c1dee3' \
--header 'Content-Type: application/json' \
--data '{
    "name": "advanced-electric_car",
    "engine" : {
        "name" : "advanced-electric_engine"
    },
    "car_user_car" : [
        {
            "user" : 1,
            "number_plate" : "ac123"
        }
    ]
}'
        """
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Test with POSTMAN
        curl --location --request PUT 'http://127.0.0.1:8000/motorizations/api/cars/134/' \
--header 'Authorization: Token be4126fdd668feda4c4a4c9b7761d5af15c1dee3' \
--header 'Content-Type: application/json' \
--data '{
    "name": "advanced-electric_car",
    "engine" : {
        "id" : 30,
        "name" : "advanced-electric_engine1"
    },
    "car_user_car" : [
        {
            "id" : 134,
            "user" : 1,
            "number_plate" : "ad123"
        }
    ]
}'
        """
        return super().update(request, *args, **kwargs)
    
    
    def get_serializer_class(self):
        request_data = self.request.data
        engine = request_data.get('engine')
        car_user_car = request_data.get('car_user_car')
        
        if car_user_car is not None and engine is not None:
            return Car__CarUser__Engine_WritableNestedSerializer
        elif engine is not None:
            return Car__Engine_WritableNestedSerializer
        elif car_user_car is not None:
            return Car__CarUser_WritableNestedSerializer
        return CarSerializer
      
    
class CarUserViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = '__all__'
    queryset = CarUser.objects.all()
    
    def get_serializer_class(self):
        request_data = self.request.data
        
        car = request_data.get('car')
        if car and isinstance(car, dict):
            engine = car.get('engine')
            if engine and isinstance(engine, dict):
                return CarUser__Car__Engine_WritableNestedSerializer
            else:
                return CarUser__Car_WritableNestedSerializer
        return CarUserValidateModelSerializer
