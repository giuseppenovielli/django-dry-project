from django.contrib.auth import get_user_model

from django_filters import rest_framework as filters

from .models import Engine, Car


class Engine_Filter(filters.FilterSet):
    user = filters.ModelChoiceFilter(field_name='user', label='User', method='user_filter', queryset=get_user_model().objects.all())
    number_plate__contains = filters.CharFilter(field_name='number plate contains', label='Number plate contains', method='number_plate__contains_filter')
    
    class Meta:
        model = Engine
        fields = '__all__'
        
    def user_filter(self, queryset, name, value):
        return queryset.user(value)

    def number_plate__contains_filter(self, queryset, name, value):
        return queryset.number_plate__contains(value)

    @property
    def qs(self):
        qs = super().qs        
        return qs


class Car_Filter(Engine_Filter):
    
    class Meta:
        model = Car
        fields = '__all__'
        
    