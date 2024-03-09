from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import *


@admin.register(Engine)
class Engine_admin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name']


@admin.register(Car)
class CarAdmin(ImportExportModelAdmin):
    raw_id_fields = ['engine']
    search_fields = ['name', 'engine__name']
    list_display = ['id', 'name', 'engine']


@admin.register(CarUser)
class CarUserAdmin(ImportExportModelAdmin):
    raw_id_fields = ['car', 'user', 'user_created']
    search_fields = ['car__name',
                     'car__engine__name',
                     'car__user__email',
                     'number_plate']
    list_display = ['id', 'car', 'user','number_plate', 'user_created', 'datetime_created']
