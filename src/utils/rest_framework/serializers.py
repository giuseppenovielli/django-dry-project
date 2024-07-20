import json
from rest_framework import serializers

from django.core.exceptions import ValidationError as DjangoValidationError, FieldDoesNotExist

class ValidateModelSerializer:
    """
    https://www.django-rest-framework.org/community/3.0-announcement/#differences-between-modelserializer-validation-and-modelform
    https://github.com/encode/django-rest-framework/discussions/7850#discussioncomment-8380135
    
    TODO -> Check support ManyToMany Relationships
    """
    
    def is_valid(self, raise_exception=False, **kwargs):
        print('ValidateModelSerializer is_valid -> {}'.format(self.Meta.model))
        
        is_valid = super().is_valid(raise_exception=raise_exception)
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
        i = model_class(**validated_data)
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
    
    
class NestedValidateModelSerializer(ValidateModelSerializer):
    """
    Support for NestedSerializer with ValidateModelSerializer
    
    TODO -> Check support ManyToMany Relationships
    """    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.nested_instances = {}
        self.is_validate_nested = False
        
    #Avaiable API
    def validate_nested(self, request_data, nested_instances) -> dict:
        """
        Validate nested serializers
        
        Add to dict 'nested_instance':
            key: model field name
            value: model instance

        Args:
            request_data (dict): data from request
            nested_instance (dict): nested instance
        """
        raise AssertionError(
            "'%s' should override the `validate_nested()` method."
            % self.__class__.__name__
        )
        
    
    def validate_attrs(self, attrs) -> dict:
        """
        Use this method instead of 'validate()'

        Args:
            attrs (dict): attrs
        """
        return attrs
        
        
    def create_nested(self, validated_data) -> None:
        """
        Save nested instance

        Args:
            validated_data (dict): validated data of serializer
        """
        model = self.Meta.model
        for key, value in validated_data.items():
            field = model._meta.get_field(key)
            if field.is_relation and not value.id:
                value.save()
                
    #
    
    def is_valid(self, raise_exception=False, **kwargs):
        # https://stackoverflow.com/questions/9436681/how-to-detect-method-overloading-in-subclasses-in-python
        if type(self).is_valid != NestedValidateModelSerializer.is_valid:
            raise AssertionError(
                    "'%s' can't override `is_valid()` method."
                    % self.__class__.__name__
                )
        attrs = self.validate(self.initial_data.copy())
        self.is_validate_nested = True
        
        kwargs = {**self.nested_instances, **kwargs}
        return super().is_valid(raise_exception, **kwargs)  
    
    
    def validate(self, attrs):
        # https://stackoverflow.com/questions/9436681/how-to-detect-method-overloading-in-subclasses-in-python
        if type(self).validate != NestedValidateModelSerializer.validate:
            raise AssertionError(
                    "'%s' override `validate_attrs()` method instead of `validate()`."
                    % self.__class__.__name__
                )
            
        if not self.is_validate_nested:
            attrs = json.loads(json.dumps(attrs))
            nested_instances = self.validate_nested(attrs, self.nested_instances)
            if not nested_instances:
                raise AssertionError(
                    "'%s' should return populated dict 'nested instances' from `validate_nested()` method."
                    % self.__class__.__name__
                )
            return attrs
        
        attrs = super().validate(attrs)
        attrs = self.validate_attrs(attrs)
        for key, value in self.nested_instances.items():
            attrs[key] = value
        return attrs
    
    
    def create(self, validated_data, **kwargs):
        self.create_nested(validated_data)      
        return super().create(validated_data, **kwargs)
    
    
    def update(self, instance, validated_data):
        if type(self).update != NestedValidateModelSerializer.update:
            raise AssertionError(
                    "'%s' can't override `is_valid()` method."
                    % self.__class__.__name__
                )
        raise serializers.ValidationError('Update not supported')