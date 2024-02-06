from django.contrib.auth import get_user_model

from django_filters import rest_framework as filters

from .models import Engine, Car


class Engine_Filter(filters.FilterSet):
    car__car_user__user = filters.ModelChoiceFilter(field_name='user', label='User', method='car__car_user__user_filter', queryset=get_user_model().objects.all())
    car__car_user__number_plate__contains = filters.CharFilter(field_name='number plate contains', label='Number plate contains', method='car__car_user__number_plate__contains_filter')
    or__car__car_user__number_plate__contains = filters.CharFilter(field_name='or number plate contains', label='OR Number plate contains', method='or__car__car_user__number_plate__contains_filter')

    class Meta:
        model = Engine
        fields = '__all__'
    
    #AND
    def car__car_user__user_filter(self, queryset, name, value):
        return queryset.car__car_user__user(value)

    def car__car_user__number_plate__contains_filter(self, queryset, name, value):
        return queryset.car__car_user__number_plate__contains(value)

    @property
    def qs(self):
        #MASTER QUERY RETURN TO VIEW
        #You can edit before return to viewset
        qs = super().qs        
        return qs


class Car_Filter(filters.FilterSet):
    car_user__user = filters.ModelChoiceFilter(field_name='user', label='User', method='car_user__user_filter', queryset=get_user_model().objects.all())
    car_user__number_plate__contains = filters.CharFilter(field_name='number plate contains', label='Number plate contains', method='car_user__number_plate__contains_filter')
    
    class Meta:
        model = Engine
        fields = '__all__'
        
    def car_user__user_filter(self, queryset, name, value):
        return queryset.car_user__user(value)

    def car_user__number_plate__contains_filter(self, queryset, name, value):
        return queryset.car_user__number_plate__contains(value)
    
    class Meta:
        model = Car
        fields = '__all__'
        
    