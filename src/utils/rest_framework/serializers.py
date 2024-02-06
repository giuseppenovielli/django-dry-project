from rest_framework import serializers

from django.core.exceptions import ValidationError as DjangoValidationError

class ValidateModelSerializer:
    
    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if not is_valid:
            return is_valid
        
        obj = self.model_instance(self.Meta.model, self.validated_data, self.instance, self.partial)
        errors = self.model_validation(obj)
        
        if errors and raise_exception:
            raise serializers.ValidationError(detail=errors)
        return 
    
    #
    
    #INSTANCE
    def model_instance(self, model_class, validated_data, instance=None, partial=False):
        if not instance:
            return self.model_instance_create(model_class, validated_data)
        return self.model_instance_update(model_class, validated_data, instance, partial)
    
    
    def model_instance_create(self, model_class, validated_data):
        obj = model_class(**validated_data)
        return obj
    
    
    def model_instance_update(self, model_class, validated_data, instance, partial=False):
        for field in instance._meta.fields:
            if field.name not in validated_data:
                continue
            setattr(instance, field.name, validated_data[field.name])
        return instance
    
    #
    
    #VALIDATION
    def model_validation_method(self, object):
        object.full_clean()
        
        
    def model_validation(self, object):
        errors = None
        try:
            self.model_validation_method(object)
        except DjangoValidationError as exc:
            errors = serializers.as_serializer_error(exc)
        return errors
    
    
    
    
