from django.db import models

from .querysets import CarQuerySet, CarUserQuerySet, EngineQuerySet

class EngineManager(models.Manager.from_queryset(EngineQuerySet)):
    pass

class CarManager(models.Manager.from_queryset(CarQuerySet)):
    pass

#https://stackoverflow.com/questions/37764070/django-migrations-valueerror-could-not-find-manager-in-django-db-models-manager
class CarUserManager(models.Manager.from_queryset(CarUserQuerySet)):
    #https://docs.djangoproject.com/en/3.2/topics/migrations/#model-managers
    use_in_migrations = True
    
    
class CarUserSuperUserManager(CarUserManager):
    
    def get_queryset(self):
        return super().get_queryset().user__is_superuser(True)
    

class CarUserExcludeSuperUserManager(CarUserManager):
    
    def get_queryset(self):
        return super().get_queryset().user__is_superuser(False)