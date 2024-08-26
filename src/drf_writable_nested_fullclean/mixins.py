# -*- coding: utf-8 -*-
"""
Giuseppe Novielli 2024 (Copyright) 
https://www.github.com/giuseppenovielli/ 


This is drf_writable_nested library:
https://github.com/beda-software/drf-writable-nested
v0.7.0

-> these simbols: ### means that some code is added for ValidateModelSerializer support <-

TESTED: 
    ForeignKey (direct/reverse)
    ManyToMany (direct/reverse excluding m2m relations with through model)
    
NOT TESTED: 
    OneToOne (direct/reverse)
    GenericRelation (this is always only reverse)
"""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from drf_writable_nested.mixins import (
    BaseNestedModelSerializer as BedaBaseNestedModelSerializer, 
    NestedCreateMixin as BedaNestedCreateMixin, 
    NestedUpdateMixin as BedaNestedUpdateMixin, 
    UniqueFieldsMixin as BedaUniqueFieldsMixin
)
from utils.rest_framework.serializers import FullCleanModelSerializer
from .utils import get_base_classes


# DEBUG
def print_debug(message):
    drf_full_clean = getattr(settings, 'DRF_WRITABLE_NESTED_FULLCLEAN', {})
    if not drf_full_clean.get('DEBUG', False):
        return
    print('\nDRF_WRITABLE_NESTED_FULLCLEAN -> {}'.format(message))
    

def get_is_allowed_partial_instances(serializer_obj):
    drf_full_clean = getattr(settings, 'DRF_WRITABLE_NESTED_FULLCLEAN', {})
    
    allow_partial_instances_serializer_meta = getattr(serializer_obj.Meta, 'allow_partial_instances', None)
    if isinstance(allow_partial_instances_serializer_meta, bool):
        return allow_partial_instances_serializer_meta
    else:
        return drf_full_clean.get('ALLOW_PARTIAL_INSTANCES', True)

class BaseNestedModelSerializer(FullCleanModelSerializer, BedaBaseNestedModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ###
        self._relations = None
        self._reverse_relations = None
        ###

    def is_valid(self, raise_exception=False, exclude=None, validate_unique=True, extra_include=None, *args, **kwargs):
        print_debug('BedaBaseNestedModelSerializer is_valid -> {}'.format(type(self)))
        is_valid = super(BedaBaseNestedModelSerializer, self).is_valid(raise_exception=raise_exception)
        if not is_valid:
            return is_valid

        print_debug('BaseNestedModelSerializer is_valid -> {}'.format(type(self)))
        
        allow_partial_instances = get_is_allowed_partial_instances(self)
        print_debug('serializer {}'.format(type(self)))
        print_debug('allow_partial_instances -> {}'.format(allow_partial_instances))
        
        validated_data = self.validated_data
        
        relations, reverse_relations = self._extract_relations(validated_data)
        
        self._relations = relations
        print_debug('direct relations -> {}'.format(relations))
        
        self._reverse_relations = reverse_relations
        print_debug('reverse relations -> {}'.format(reverse_relations))
        
        #
        
        # Create or update direct relations (foreign key, one-to-one)
        direct_relations_obj = self.update_or_create_direct_relations(
            validated_data,
            relations,
            not allow_partial_instances
        )
        
        #
        
        #Validate model fields
        if not extra_include or not isinstance(extra_include, dict):
            extra_include = {}
    
        # Add to extra include all direct relations (partial instances)
        if allow_partial_instances:
            extra_include.update(direct_relations_obj)
        
        #

        is_valid = super().is_valid(raise_exception=raise_exception, 
                                    exclude=exclude, validate_unique=validate_unique, 
                                    extra_include=extra_include, 
                                    *args, **kwargs)
        if not is_valid:
            return is_valid
        
        #
        
        # if not allow_partial_instances not check reverse relations
        if not allow_partial_instances:
            return is_valid
        
        #

        #Partial Instance
        instance = self.Meta.model(**validated_data)
        for key, value in extra_include.items():
            setattr(instance, key, value)
        
        #
        
        # Update or create reverse relations
        self.update_or_create_reverse_relations(
            instance,
            reverse_relations
        )
        return is_valid
    
    #
    
    #Override method from BaseNestedModelSerializer
    def update_or_create_reverse_relations(self, instance, reverse_relations):
        # Update or create reverse relations:
        # many-to-one, many-to-many, reversed one-to-one
        for field_name, (related_field, field, field_source) in \
                reverse_relations.items():

            # Skip processing for empty data or not-specified field.
            # The field can be defined in validated_data but isn't defined
            # in initial_data (for example, if multipart form data used)
            related_data = self.get_initial().get(field_name, None)
            if related_data is None:
                continue

            if related_field.one_to_one:
                # If an object already exists, fill in the pk so
                # we don't try to duplicate it
                pk_name = field.Meta.model._meta.pk.attname
                if pk_name not in related_data and 'pk' in related_data:
                    pk_name = 'pk'
                if pk_name not in related_data:
                    related_instance = getattr(instance, field_source, None)
                    if related_instance:
                        related_data[pk_name] = related_instance.pk

                # Expand to array of one item for one-to-one for uniformity
                related_data = [related_data]

            instances = self._prefetch_related_instances(field, related_data)

            ###
            save_kwargs = {}
            if instance.id:
                save_kwargs = self._get_save_kwargs(field_name)
            ###
             
            if isinstance(related_field, GenericRelation):
                save_kwargs.update(
                    self._get_generic_lookup(instance, related_field),
                )
            elif not related_field.many_to_many:
                save_kwargs[related_field.name] = instance

            new_related_instances = []
            errors = []

            for data in related_data:
                obj = instances.get(
                    self._get_related_pk(data, field.Meta.model)
                )
                serializer = self._get_serializer_for_field(
                    field,
                    instance=obj,
                    data=data,
                )
                
                ###
                extra_include = None
                if FullCleanModelSerializer in get_base_classes(serializer):
                    if save_kwargs:
                        extra_include = save_kwargs
                    else:                   
                        #Extract name of related field from related model that is the same as instance
                        for field_item in field.Meta.model._meta.get_fields():
                            if field_item.is_relation and field_item.related_model == self.Meta.model:
                                if extra_include:
                                    raise Exception('Model {} has more than one relation with model {}'.format(self.Meta.model, field_item.related_model))
                                extra_include = {field_item.name : instance}
                                break
                    
                try:
                    if extra_include:
                        serializer.is_valid(raise_exception=True, extra_include=extra_include)
                    else:
                        serializer.is_valid(raise_exception=True)
                        
                    errors.append({})
                    
                    if instance.id:
                        related_instance = serializer.save(**save_kwargs)
                        data['pk'] = related_instance.pk
                        new_related_instances.append(related_instance)
                
                except ValidationError as exc:
                    errors.append(exc.detail)
                ###
                
            if any(errors):
                if related_field.one_to_one:
                    raise ValidationError({field_name: errors[0]})
                else:
                    raise ValidationError({field_name: errors})
            
            ###
            if instance.id and related_field.many_to_many:
                # Add m2m instances to through model via add
                m2m_manager = getattr(instance, field_source)
                m2m_manager.add(*new_related_instances)
            ###
                
                
    def update_or_create_direct_relations(self, attrs, relations, save=True):
        ###
        direct_relations = {}
        ###
        
        for field_name, (field, field_source) in relations.items():
            obj = None
            data = self.get_initial()[field_name]
            model_class = field.Meta.model
            pk = self._get_related_pk(data, model_class)
            if pk:
                obj = model_class.objects.filter(
                    pk=pk,
                ).first()
            serializer = self._get_serializer_for_field(
                field,
                instance=obj,
                data=data,
            )

            try:
                serializer.is_valid(raise_exception=True)
                ###
                if save:
                    save_kwargs = getattr(self, '_save_kwargs', {})
                    if save_kwargs:
                        save_kwargs = self._get_save_kwargs(field_name)
                    else:
                        save_kwargs = serializer.validated_data
                        
                    i = serializer.save(**save_kwargs)
                    attrs[field_source] = i
                else:
                    i = model_class(**serializer.validated_data)
                
                direct_relations[field_name] = i
                ###
                
            except ValidationError as exc:
                raise ValidationError({field_name: exc.detail})
            
        ###
        return direct_relations
        ###
    
    
class NestedCreateMixin(BedaNestedCreateMixin, BaseNestedModelSerializer):
    
    def create(self, validated_data):
        print_debug('NestedCreateMixin Create -> {}'.format(self))
        
        ###
        # relations, reverse_relations = self._extract_relations(validated_data)###

        # Create or update direct relations (foreign key, one-to-one)
        allow_partial_instances = get_is_allowed_partial_instances(self)
        if allow_partial_instances:
            self.update_or_create_direct_relations(
                validated_data,
                self._relations,
            )
        ###

        # Create instance
        instance = super(BedaBaseNestedModelSerializer, self).create(validated_data)

        ###
        self.update_or_create_reverse_relations(instance, self._reverse_relations)
        ###
        
        return instance
    

class NestedUpdateMixin(BedaNestedUpdateMixin, BaseNestedModelSerializer):
    
    def update(self, instance, validated_data):
        print_debug('NestedUpdateMixin Update -> {}'.format(self))
        
        ###
        # relations, reverse_relations = self._extract_relations(validated_data)
        relations = self._relations
        reverse_relations = self._reverse_relations

        allow_partial_instances = get_is_allowed_partial_instances(self)
        if allow_partial_instances:
            # Create or update direct relations (foreign key, one-to-one)
            self.update_or_create_direct_relations(
                validated_data,
                relations,
            )
        ###
        
        
        # Update instance
        instance = super(BedaBaseNestedModelSerializer, self).update(
            instance,
            validated_data,
        )
        self.update_or_create_reverse_relations(instance, reverse_relations)
        self.delete_reverse_relations_if_need(instance, reverse_relations)
        instance.refresh_from_db()
        return instance
    
    
class UniqueFieldsMixin(BedaUniqueFieldsMixin):
    ###
    def is_valid(self, raise_exception=False, *args, **kwargs):
        print_debug('BedaUniqueFieldsMixin is_valid -> {}'.format(type(self)))
        is_valid = super().is_valid(raise_exception, *args, **kwargs)
        if not is_valid:
            return is_valid
        
        print_debug('UniqueFieldsMixin is_valid -> {}'.format(type(self)))
        self._validate_unique_fields(self.validated_data)
    ###