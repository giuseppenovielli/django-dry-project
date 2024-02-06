from rest_framework import serializers
from django.utils import timezone

from users.serializers import UserSerializer
from utils.rest_framework.serializers import ValidateModelSerializer

from .models import Engine, Car, Car_user

class Engine_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = Engine
        fields = '__all__'
        

class Car_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = Car
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['engine'] = Engine_Serializer(instance.engine).data
        return representation
    
        

class Car_user_Serializer(ValidateModelSerializer, serializers.ModelSerializer):
    
    class Meta:
        model = Car_user
        fields = '__all__'
        #https://www.django-rest-framework.org/api-guide/serializers/#specifying-read-only-fields
        read_only_fields = ['user_created', 'datetime_created']
      
    def to_representation(self, instance):
        """
        https://testdriven.io/tips/ed79fa08-6834-4827-b00d-2609205129e0/
        
        If you want to change the output, when this serializer is used also for POST, PATCH or PUT, you can override the to_representation function.
        """
        representation = super().to_representation(instance)
        representation['car'] = Car_Serializer(instance.car, context=self.context).data
        representation['user'] = UserSerializer(instance.user, context=self.context).data
        return representation


    
    def validate(self, attrs):
        """
        https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
        The main validations for object Car_user is stored into models class, ONE PLACE (DRY)
        """
        request = self.context['request']
        
        #Set the read_only fields values
        attrs['user_created'] = request.user
        attrs['datetime_created'] = timezone.now()
        return super().validate(attrs)
    
    