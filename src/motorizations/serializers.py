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
    
    
    def is_valid(self, raise_exception=False, **kwargs):
        is_valid = super().is_valid(raise_exception, **kwargs)
        if not is_valid:
            return is_valid
        
        self.car_users_is_valid()
        return is_valid
    
    
    def create(self, validated_data):
        car = super().create(validated_data)
        self.car_users_create(car)
        return car
    
    
    def car_users_is_valid(self):
        if self.instance:
            return
        
        car = self.Meta.model(**self.validated_data)
        
        context = self.context
        request = context['request']
        
        serializers_car_user = []
        for car_user_dict in request.data.get('car_users', []):
            s = CarUser_CarExcluded_Serializer(data=car_user_dict, context=context)
            s.is_valid(raise_exception=True, car=car)
            serializers_car_user.append(s)
        context['car_user_serialzers'] = serializers_car_user
        
    
    def car_users_create(self, car):
        car_users_serializers = self.context.get('car_user_serialzers', [])
        for s in car_users_serializers:
            s.save(car=car)
     
            
#
   
   
#CarUser
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
        request = self.context['request']
        
        #Set the read_only fields values
        attrs['user_created'] = request.user
        return super().validate(attrs)
    
    
class CarUser_CarExcluded_Serializer(CarUserSerializer):
        
    class Meta:
        model = CarUser
        fields = ('pk', 'user', 'number_plate',)
        

class CarUser_CarNested_Serializer(CarUser_CarExcluded_Serializer):
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        
        context = self.context
        if context.get('car'):
            return attrs
        
        s = CarSerializer(data=attrs.get('car'), context=self.context)
        s.is_valid(raise_exception=True)
        context['car'] = Car(**s.validated_data)
        
        return attrs
    
    def is_valid(self, raise_exception=False, **kwargs):
        self.validate(self.initial_data)
        
        context = self.context
        car = context['car']
        
        return super().is_valid(raise_exception, car=car, **kwargs)
    
    
    def create(self, validated_data):
        car = self.context['car']
        car.save()
        validated_data['car'] = car
        
        return super().create(validated_data)


#


#WRITEBLE NESTED SERIALIZER
class Engine_writable_nested_Serializer(WritableNestedModelSerializer): 
    class Meta:
        model = Engine
        fields = ['pk', 'name']
        


class Car_CarUserWritableNestedSerializer(WritableNestedModelSerializer):
    """
Traceback (most recent call last):
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/rest_framework/serializers.py", line 962, in create
    instance = ModelClass._default_manager.create(**validated_data)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/django/db/models/query.py", line 451, in create
    obj = self.model(**kwargs)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/django/db/models/base.py", line 503, in __init__
    raise TypeError("%s() got an unexpected keyword argument '%s'" % (cls.__name__, kwarg))
TypeError: Car() got an unexpected keyword argument 'car_users'
    """
    #engine = Engine_writable_nested_Serializer()
    car_users = CarUser_CarExcluded_Serializer(many=True)

    class Meta:
        model = Car
        fields = ('pk', 'name', 'engine', 'car_users',)



class CarUser_WritableNestedSerializer(WritableNestedModelSerializer):
    """
    ISSUE
    If Car_User.clean() raise an exception, but Car.clean() doesn't, Car will be saved into db but without Car_User
    WORKAROUND
    use -> CarUser_CarNested_Serializer
    """
    car = CarSerializer()
    
    class Meta:
        model = CarUser
        fields = ('id', 'user', 'car', 'number_plate',)
        read_only_fields = ['user_created', 'datetime_created']
    
    
    def validate(self, attrs):
        request = self.context['request']
        
        #Set the read_only fields values
        attrs['user_created'] = request.user
        return super().validate(attrs)
    