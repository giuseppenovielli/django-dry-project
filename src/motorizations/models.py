from django.db import models

from django.contrib.auth import get_user_model 

from .managers import *

User = get_user_model()

# Create your models here.
class Engine(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')

    objects = Engine_QuerySet.as_manager()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Engine'
        verbose_name_plural = 'Engines'
        
    def __str__(self):
        return '{}'.format(self.name)
    
class Car(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE, verbose_name='Engine')

    objects = Car_QuerySet.as_manager()
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self):
        return '{} {}'.format(self.name, self.engine)
    
    
class Car_user(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Car')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    number_plate = models.CharField(max_length=10, verbose_name='Number plate')
    
    objects = Car_user_QuerySet.as_manager()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Car bouth by user'
        verbose_name_plural = 'Cars bouth by users'
        unique_together = ['car', 'user', 'number_plate']
    
    def __str__(self):
        return '{} {} {}'.format(self.car, self.user, self.number_plate)