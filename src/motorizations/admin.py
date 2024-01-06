from django.contrib import admin

from .models import *

# Register your models here.
class Engine_admin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name']

admin.site.register(Engine, Engine_admin)


class Car_admin(admin.ModelAdmin):
    raw_id_fields = ['engine']
    search_fields = ['name', 'engine__name']
    list_display = ['id', 'name', 'engine']

admin.site.register(Car, Car_admin)


class Car_user_admin(admin.ModelAdmin):
    raw_id_fields = ['car', 'user']
    search_fields = ['car__name',
                     'car__engine__name',
                     'car__user__email',
                     'number_plate']
    list_display = ['id', 'car', 'user','number_plate']

admin.site.register(Car_user, Car_user_admin)