from rest_framework import serializers

from drf_writable_nested.mixins import UniqueFieldsMixin

from drf_writable_nested_fullclean.serializers import WritableNestedFullCleanSerializer

from users.serializers import UserSerializer
from utils.rest_framework.serializers import FullCleanModelSerializer

from .models import Engine, Car, CarUser

# Base serializers
class EngineSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Engine
        fields = '__all__'

class EngineValidateModelSerializer(FullCleanModelSerializer, EngineSerializer):
    pass

class CarSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Car
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['engine'] = EngineSerializer(instance.engine).data
        return representation
    
class CarValidateModelSerializer(FullCleanModelSerializer, CarSerializer):
    pass
            

class CarUserSerializer(serializers.ModelSerializer):
    
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
        attrs = super().validate(attrs)
        
        #Set the read_only fields values
        attrs['user_created'] = self.context['request'].user
        return attrs
  

class CarUserValidateModelSerializer(FullCleanModelSerializer, CarUserSerializer):
    pass
#


# WRITEBLE NESTED SERIALIZER

# Car
class Car__Engine_WritableNestedSerializer(WritableNestedFullCleanSerializer):
    # Direct FK relation
    engine = EngineValidateModelSerializer()
    
    class Meta:
        model = Car
        fields = ('id', 'name', 'engine',)

class CarUser_CarExcluded_Serializer(CarUserValidateModelSerializer):
        
    class Meta:
        model = CarUser
        fields = ('id', 'user', 'number_plate',)
        
class Car__CarUser_WritableNestedSerializer(WritableNestedFullCleanSerializer):
    # Reverse FK relation
    car_user_car = CarUser_CarExcluded_Serializer(many=True)
    
    class Meta:
        model = Car
        fields = ('id', 'name', 'car_user_car',)
        
class Car__CarUser__Engine_WritableNestedSerializer(Car__Engine_WritableNestedSerializer, Car__CarUser_WritableNestedSerializer):
    class Meta:
        model = Car
        fields = ('id', 'name', 'engine', 'car_user_car',)

#


# CarUser
class CarUser__Car_WritableNestedSerializer(WritableNestedFullCleanSerializer, CarUserSerializer):
    # Direct FK relation
    car = CarValidateModelSerializer()

    class Meta:
        model = CarUser
        fields = ('id', 'user', 'number_plate', 'car',)
    
    
class CarUser__Car__Engine_WritableNestedSerializer(CarUser__Car_WritableNestedSerializer):
    # Direct FK relation Nested
    car = Car__Engine_WritableNestedSerializer()
    