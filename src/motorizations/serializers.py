from rest_framework import serializers

from .models import Engine, Car, Car_user

class Engine_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = Engine
        fields = '__all__'
        

class Car_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = Car
        fields = '__all__'
        

class Car_user_Serializer(serializers.ModelSerializer): 
    class Meta:
        model = Car_user
        fields = '__all__'