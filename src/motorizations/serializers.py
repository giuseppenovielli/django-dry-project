from rest_framework import serializers
from django.utils import timezone

from drf_writable_nested.serializers import WritableNestedModelSerializer

from users.serializers import UserSerializer
from utils.rest_framework.serializers import NestedValidateModelSerializer, ValidateModelSerializer

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
        attrs = super().validate(attrs)
        
        #Set the read_only fields values
        attrs['user_created'] = self.context['request'].user
        return attrs
  

class CarUserValidateModelSerializer(ValidateModelSerializer, CarUserSerializer):
    pass
      
        
class CarUser_CarExcluded_Serializer(CarUserValidateModelSerializer):
        
    class Meta:
        model = CarUser
        fields = ('pk', 'user', 'number_plate',)
        

class CarUser_CarNested_Serializer(NestedValidateModelSerializer, CarUser_CarExcluded_Serializer):
    
    def validate_nested(self, request_data, nested_instances) -> dict:
        s = CarSerializer(data=request_data.get('car'), context=self.context)
        s.is_valid(raise_exception=True)
        nested_instances['car'] = Car(**s.validated_data)
        return nested_instances

#


#WRITEBLE NESTED SERIALIZER
class Engine_writable_nested_Serializer(WritableNestedModelSerializer): 
    class Meta:
        model = Engine
        fields = ['pk', 'name']
        


class Car_CarUserWritableNestedSerializer(WritableNestedModelSerializer):
    """
    Internal Server Error: /motorizations/api/cars/
Traceback (most recent call last):
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/django/core/handlers/exception.py", line 47, in inner
    response = get_response(request)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/django/core/handlers/base.py", line 181, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/django/views/decorators/csrf.py", line 54, in wrapped_view
    return view_func(*args, **kwargs)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/rest_framework/viewsets.py", line 125, in view
    return self.dispatch(request, *args, **kwargs)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/rest_framework/views.py", line 509, in dispatch
    response = self.handle_exception(exc)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/rest_framework/views.py", line 469, in handle_exception
    self.raise_uncaught_exception(exc)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/rest_framework/views.py", line 480, in raise_uncaught_exception
    raise exc
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/rest_framework/views.py", line 506, in dispatch
    response = handler(request, *args, **kwargs)
  File "/Users/hrcoffee6/django_dry_project/src/motorizations/views.py", line 44, in create
    return super().create(request, *args, **kwargs)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/rest_framework/mixins.py", line 19, in create
    self.perform_create(serializer)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/rest_framework/mixins.py", line 24, in perform_create
    serializer.save()
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/drf_writable_nested/mixins.py", line 234, in save
    return super(BaseNestedModelSerializer, self).save(**kwargs)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/rest_framework/serializers.py", line 212, in save
    self.instance = self.create(validated_data)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/drf_writable_nested/mixins.py", line 262, in create
    self.update_or_create_reverse_relations(instance, reverse_relations)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/drf_writable_nested/mixins.py", line 166, in update_or_create_reverse_relations
    instances = self._prefetch_related_instances(field, related_data)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/drf_writable_nested/mixins.py", line 128, in _prefetch_related_instances
    pk_list = self._extract_related_pks(field, related_data)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/drf_writable_nested/mixins.py", line 120, in _extract_related_pks
    pk = self._get_related_pk(d, model_class)
  File "/Users/hrcoffee6/my_venv/django_3/lib/python3.9/site-packages/drf_writable_nested/mixins.py", line 109, in _get_related_pk
    pk = data.get('pk') or data.get(model_class._meta.pk.attname)
AttributeError: 'str' object has no attribute 'get'
    """
    #engine = Engine_writable_nested_Serializer()
    car_user = CarUser_CarExcluded_Serializer()

    class Meta:
        model = Car
        fields = ('pk', 'name', 'engine', 'car_user',)



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
    