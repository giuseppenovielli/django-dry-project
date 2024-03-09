from rest_framework import serializers

from django.core.exceptions import ValidationError as DjangoValidationError, FieldDoesNotExist

class ValidateModelSerializer:
    """
    https://www.django-rest-framework.org/community/3.0-announcement/#differences-between-modelserializer-validation-and-modelform
    https://github.com/encode/django-rest-framework/discussions/7850#discussioncomment-8380135
    """
    
    def is_valid(self, raise_exception=False, **kwargs):
        is_valid = super().is_valid(raise_exception)
        print('is_valid {} = {}'.format(is_valid, self.Meta.model))
        if not is_valid:
            return is_valid
        
        obj = self.model_instance(self.Meta.model, self.validated_data, self.instance, self.partial, **kwargs)
        if obj:
            errors = self.model_validation(obj, **kwargs)
        else:
            raise Exception('Nested serializers are not supported.')
        
        if errors and raise_exception:
            raise serializers.ValidationError(detail=errors)
        return not errors
    
    #
    
    #INSTANCE
    def model_instance(self, model_class, validated_data, instance=None, partial=False, **kwargs):
        if not instance:
            return self.model_instance_create(model_class, validated_data, **kwargs)
        return self.model_instance_update(model_class, validated_data, instance, partial, **kwargs)
    
    
    def model_instance_create(self, model_class, validated_data, **kwargs):
        try:
            i = model_class(**validated_data)
        except:
            return
        
        #Add fields value that are not in validated_data
        if kwargs:
            for key,value in kwargs.items():
                setattr(i, key, value)
        return i
        
    
    
    def model_instance_update(self, model_class, validated_data, instance, partial=False, **kwargs):
        try:
            for field in instance._meta.fields:
                if field.name not in validated_data:
                    continue
                setattr(instance, field.name, validated_data[field.name])
        except:
            return
        
        #Add fields value that are not in validated_data
        if kwargs:
            for key,value in kwargs.items():
                setattr(instance, key, value)
        return instance
        
    
    #
    
    #VALIDATION
    def model_validation_method(self, object, **kwargs):
        exclude = []
        
        if kwargs:
            for key,value in kwargs.items():
                try:
                    field = object._meta.get_field(key)
                    exclude.append(key)
                    print(field)
                    if field.is_relation and bool(field.validators):
                        raise Exception('Unsupported validation! Field {} is a relation that contains validators that needs the database id. Try to move validations\'s logic into clean() method, but analize object\'s fields instead make a query to the database, that validators need'.format(key))
                except FieldDoesNotExist:
                    pass
                
        object.full_clean(exclude=exclude)
        
        
    def model_validation(self, object, **kwargs):
        try:
            self.model_validation_method(object, **kwargs)
        except DjangoValidationError as exc:
            return serializers.as_serializer_error(exc)
    
    
    
    
