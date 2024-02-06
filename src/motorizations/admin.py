from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from import_export.admin import ImportExportModelAdmin

from .models import *

# Register your models here.
class Engine_admin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name']

admin.site.register(Engine, Engine_admin)


class Car_admin(ImportExportModelAdmin):
    raw_id_fields = ['engine']
    search_fields = ['name', 'engine__name']
    list_display = ['id', 'name', 'engine']

admin.site.register(Car, Car_admin)


class Car_user_admin(ImportExportModelAdmin):
    raw_id_fields = ['car', 'user', 'user_created']
    search_fields = ['car__name',
                     'car__engine__name',
                     'car__user__email',
                     'number_plate']
    list_display = ['id', 'car', 'user','number_plate', 'user_created', 'datetime_created']

admin.site.register(Car_user, Car_user_admin)