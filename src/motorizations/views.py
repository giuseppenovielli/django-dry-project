from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from .models import Engine, Car, CarUser
from .serializers import CarUserExcludeCarSerializer, EngineSerializer, CarSerializer, CarUserSerializer
from .filters import EngineFilter, CarFilter

from rest_framework import status
from rest_framework.response import Response

class EngineViewSet(viewsets.ModelViewSet):
    serializer_class = EngineSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = EngineFilter
    queryset = Engine.objects.all()
    

class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CarFilter
    queryset = Car.objects.all()
    
    def _writable_many_car_user(self, request):
        s_context = self.get_serializer_context()
        
        s_car = self.get_serializer(data=request.data,context=s_context)
        s_car.is_valid(raise_exception=True)
        car = Car(**s_car.validated_data)
        
        serializers_car_user = []
        for car_user_dict in request.data.get('car_user', []):
            s_car_user = CarUserExcludeCarSerializer(data=car_user_dict, context=s_context)
            s_car_user.is_valid(raise_exception=True, car=car)
            serializers_car_user.append(s_car_user)
        
        car = s_car.save()
        for s_car_user in serializers_car_user:
            s_car_user.save(car=car)
        
        respose_data=s_car.data
        return Response(respose_data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(respose_data))
        
        
    def create(self, request, *args, **kwargs):
        """
        Test with POSTMAN

        curl --location 'http://127.0.0.1:8000/motorizations/api/cars/?writable_car_user=true' \
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
            "number_plate": "admin345"
        }
    ]
}'
        """
        if request.query_params.get('writable_car_user'):
            return self._writable_many_car_user(request)
        return super().create(request, *args, **kwargs)
    
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
        
    
class CarUserViewSet(viewsets.ModelViewSet):
    serializer_class = CarUserSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = '__all__'
    queryset = CarUser.objects.all()