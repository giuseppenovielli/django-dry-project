from typing import Any
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.core.validators import RegexValidator
from utils.django.models import get_user_model

from utils.django.validators import user_is_active_validator

from .validators import user_write_authorization_validator

from .managers import *

User = get_user_model()

#https://medium.com/@rui.jorge.rei/today-i-learned-django-queryset-default-ordering-is-no-ordering-416547ee946f

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
    number_plate = models.CharField(max_length=10, verbose_name='Number plate',
                                    validators=[RegexValidator(regex=r'^[0-9a-zA-Z]*$')],
                                    )
    
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, 
                                     verbose_name='User', 
                                     related_name='car_user_created', 
                                     validators=[user_write_authorization_validator, user_is_active_validator])
    datetime_created = models.DateTimeField(default=timezone.now, verbose_name='Datetime')
    
    objects = Car_user_QuerySet.as_manager()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Car bouth by user'
        verbose_name_plural = 'Cars bouth by users'
        unique_together = ['car', 'user', 'number_plate']
        
        
    def _number_plate_user_validator(self):
        user = self.user
        last_name = user.last_name
        first_name = user.first_name
        fullname = '{} {}'.format(last_name, first_name)
        
        for number_plate_char in list(self.number_plate.lower()):
            if number_plate_char in list(fullname.lower()):
                return
        raise ValidationError(_('The name of the user must be included in the number plate'))
        

    #https://stackoverflow.com/questions/61507845/model-clean-vs-model-clean-fields
    def clean(self):
        """
        Validate rules for multiple fields before save it
        https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.clean
        """
        super().clean()
        self._number_plate_user_validator()
    
        
    def __str__(self):
        return '{} {} {}'.format(self.car, self.user, self.number_plate)