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
    
NOT TESTED: 
    OneToOne (direct/reverse)
    ManyToMany (direct/reverse excluding m2m relations with through model)
    GenericRelation (this is always only reverse)
"""
from collections import OrderedDict

from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from drf_writable_nested.mixins import BaseNestedModelSerializer, NestedCreateMixin, NestedUpdateMixin

from utils.python.classes import get_base_classes
from utils.rest_framework.serializers import FullCleanModelSerializer


class BaseNestedFullCleanSerializer(FullCleanModelSerializer, BaseNestedModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ###
        self._relations = None
        self._reverse_relations = None
        ###

    def is_valid(self, raise_exception=False, exclude=None, validate_unique=True, extra_include=None, *args, **kwargs):
        is_valid = super(BaseNestedModelSerializer, self).is_valid(raise_exception=raise_exception)
        if not is_valid:
            return is_valid
    
        validated_data = self.validated_data
        relations, reverse_relations = self._extract_relations(validated_data)
        self._relations = relations
        self._reverse_relations = reverse_relations
        
        #
        
        # Create or update direct relations (foreign key, one-to-one)
        direct_relations_obj = self.update_or_create_direct_relations(
            validated_data,
            relations,
            save=False
        )
        
        #
        
        #Validate model fields
        if not extra_include or not isinstance(extra_include, dict):
            extra_include = {}
    

        extra_include.update(direct_relations_obj)
        
        #

        is_valid = super().is_valid(raise_exception=raise_exception, 
                                    exclude=exclude, validate_unique=validate_unique, 
                                    extra_include=extra_include, 
                                    *args, **kwargs)
        if not is_valid:
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
                    i = serializer.save(**self._get_save_kwargs(field_name))
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
    
    
class NestedCreateFullCleanMixin(NestedCreateMixin, BaseNestedFullCleanSerializer):
    
    def create(self, validated_data):
        ###relations, reverse_relations = self._extract_relations(validated_data)###

        # Create or update direct relations (foreign key, one-to-one)
        ###
        self.update_or_create_direct_relations(
            validated_data,
            self._relations,
        )
        ###

        # Create instance
        instance = super(BaseNestedFullCleanSerializer, self).create(validated_data)

        ###
        self.update_or_create_reverse_relations(instance, self._reverse_relations)
        ###
        
        return instance
    

class NestedUpdateFullCleanMixin(NestedUpdateMixin, BaseNestedFullCleanSerializer):
    
    def update(self, instance, validated_data):
        ###
        # relations, reverse_relations = self._extract_relations(validated_data)
        relations = self._relations
        reverse_relations = self._reverse_relations
        ###
        
        # Create or update direct relations (foreign key, one-to-one)
        self.update_or_create_direct_relations(
            validated_data,
            relations,
        )

        # Update instance
        instance = super(BaseNestedFullCleanSerializer, self).update(
            instance,
            validated_data,
        )
        self.update_or_create_reverse_relations(instance, reverse_relations)
        self.delete_reverse_relations_if_need(instance, reverse_relations)
        instance.refresh_from_db()
        return instance
        # Reverse `reverse_relations` for correct delete priority
        reverse_relations = OrderedDict(
            reversed(list(reverse_relations.items())))

        # Delete instances which is missed in data
        for field_name, (related_field, field, field_source) in \
                reverse_relations.items():
            model_class = field.Meta.model

            related_data = self.get_initial()[field_name]
            # Expand to array of one item for one-to-one for uniformity
            if related_field.one_to_one:
                related_data = [related_data]

            # M2M relation can be as direct or as reverse. For direct relation
            # we should use reverse relation name
            if related_field.many_to_many:
                related_field_lookup = {
                    related_field.remote_field.name: instance,
                }
            elif isinstance(related_field, GenericRelation):
                related_field_lookup = \
                    self._get_generic_lookup(instance, related_field)
            else:
                related_field_lookup = {
                    related_field.name: instance,
                }

            current_ids = self._extract_related_pks(field, related_data)

            try:
                pks_to_delete = list(
                    model_class.objects.filter(
                        **related_field_lookup
                    ).exclude(
                        pk__in=current_ids
                    ).values_list('pk', flat=True)
                )
                self.perform_nested_delete_or_update(
                    pks_to_delete,
                    model_class,
                    instance,
                    related_field,
                    field_source
                )

            except ProtectedError as e:
                instances = e.args[1]
                self.fail('cannot_delete_protected', instances=", ".join([
                    str(instance) for instance in instances]))