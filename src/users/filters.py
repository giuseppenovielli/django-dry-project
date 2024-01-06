from django.contrib.auth import get_user_model

from django_filters import rest_framework as filters

User = get_user_model()

class User_Filter(filters.FilterSet):
    motorizations___car_user__in = filters.BooleanFilter(field_name='cars users IN', label='IN Car User', method='motorizations___car_user__in_filter')
    motorizations___car_user__number_plate__contains = filters.CharFilter(field_name='number plate contains', label='Number plate contains', method='motorizations___car_user__number_plate__contains_filter')

    class Meta:
        model = User
        fields = '__all__'
    
    #AND
    def motorizations___car_user__in_filter(self, queryset, name, value):
        if value:
            return queryset.motorizations___car_user__in()
        return queryset.motorizations___car_user__exclude()
    
    def motorizations___car_user__number_plate__contains_filter(self, queryset, name, value):
        return queryset.motorizations___car_user__number_plate__contains(value)