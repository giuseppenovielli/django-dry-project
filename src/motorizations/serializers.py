from rest_framework import serializers
from django.utils import timezone

from drf_writable_nested.serializers import WritableNestedModelSerializer

from users.serializers import UserSerializer
from utils.rest_framework.serializers import ValidateModelSerializer

from .models import Engine, Car, CarUser

class EngineSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Engine
        fields = '__all__'
    
    
#Car
class CarSerializer(ValidateModelSerializer, serializers.ModelSerializer): 
    class Meta:
        model = Car
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['engine'] = EngineSerializer(instance.engine).data
        return representation
    

#CarUser
class CarUserSerializer(ValidateModelSerializer, serializers.ModelSerializer):
        
    class Meta:
        model = CarUser
        fields = ('id', 'user', 'car', 'number_plate',)
        #https://www.django-rest-framework.org/api-guide/serializers/#specifying-read-only-fields
        read_only_fields = ['user_created', 'datetime_created']
      
    def to_representation(self, instance):
        """
        https://testdriven.io/tips/ed79fa08-6834-4827-b00d-2609205129e0/
        
        If you want to change the output, when this serializer is used also for POST, PATCH or PUT, you can override the to_representation function.
        """
        representation = super().to_representation(instance)
        representation['car'] = CarSerializer(instance.car, context=self.context).data
        representation['user'] = UserSerializer(instance.user, context=self.context).data
        return representation
      
    def validate(self, attrs):
        """
        https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
        The main validations for object CarUser is stored into models class, ONE PLACE (DRY)
        
        https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-editing/#models-and-request-user
        """
        request = self.context['request']
        
        #Set the read_only fields values
        attrs['user_created'] = request.user
        attrs['datetime_created'] = timezone.now()
        return super().validate(attrs)
    
    
class CarUserExcludeCarSerializer(CarUserSerializer):
        
    class Meta(CarUserSerializer.Meta):
        fields = ('user', 'number_plate',)
      

#

#WRITEBLE NESTED SERIALIZER
class Engine_writable_nested_Serializer(WritableNestedModelSerializer): 
    class Meta:
        model = Engine
        fields = ['pk', 'name']
        

class Car_writable_nested_Serializer(WritableNestedModelSerializer): 
    #engine = Engine_writable_nested_Serializer()
    car_user = CarUserSerializer(many=True)

    class Meta:
        model = Car
        fields = ('id', 'name', 'engine', 'car_user',)


class Car_user_writable_nested_Serializer(WritableNestedModelSerializer):
    car = Car_writable_nested_Serializer()
    
    class Meta:
        model = CarUser
        fields = ['id', 'user', 'number_plate']
        
      
    