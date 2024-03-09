from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from import_export.admin import ImportExportModelAdmin

from utils.django.models import get_user_model


class UserImportExportModelAdmin(ImportExportModelAdmin, UserAdmin):
    list_display = ('id',) + UserAdmin.list_display 
admin.site.register(get_user_model(), UserImportExportModelAdmin)


class GroupImportExportModelAdmin(ImportExportModelAdmin, GroupAdmin):
    pass
admin.site.unregister(Group)
admin.site.register(Group, GroupImportExportModelAdmin)