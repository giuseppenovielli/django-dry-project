from typing import Collection
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.core.validators import RegexValidator, MinLengthValidator

from utils.django.models import get_user_model
from utils.django.validators import user_is_active_validator

from .validators import user_write_authorization_validator

from .managers import CarManager, CarUserExcludeSuperUserManager, CarUserManager, CarUserSuperUserManager, EngineManager

User = get_user_model()

#https://medium.com/@rui.jorge.rei/today-i-learned-django-queryset-default-ordering-is-no-ordering-416547ee946f

#https://capitalnumbers.medium.com/django-best-practices-code-structure-naming-conventions-and-design-patterns-fe572c547755

#https://docs.djangoproject.com/en/3.2/ref/models/options/#django.db.models.Options.ordering -> SEE WARNING SECTION


# Create your models here.
class Engine(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')

    objects = EngineManager()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Engine'
        verbose_name_plural = 'Engines'
        
    def __str__(self):
        return '{}'.format(self.name)
    
class Car(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name', validators=[MinLengthValidator(10)])
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE, verbose_name='Engine')

    objects = CarManager()
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'


    def __str__(self):
        return '{} {}'.format(self.name, self.engine)
    
    
class CarUser(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Car', related_name='car_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    number_plate = models.CharField(max_length=10, verbose_name='Number plate',
                                    validators=[RegexValidator(regex=r'^[0-9a-zA-Z]*$')],
                                    )
    
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, 
                                     verbose_name='User created', 
                                     related_name='car_user_created', 
                                     validators=[user_write_authorization_validator, user_is_active_validator])
    datetime_created = models.DateTimeField(default=timezone.now, verbose_name='Datetime')
    
    #https://docs.djangoproject.com/en/3.2/topics/db/managers/#from-queryset
    objects = CarUserManager()
    superuser_objects = CarUserSuperUserManager()
    exclude_superuser_objects = CarUserExcludeSuperUserManager()

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
    
    
    def _car_user_validator(self):
        user = self.user
        last_name = user.last_name
        first_name = user.first_name
        fullname = '{} {}'.format(last_name, first_name)
        
        for car_name_char in list(self.car.name.lower()):
            if car_name_char in list(fullname.lower()):
                return
        raise ValidationError(_('The name of the car must be included in the user name'))
        

    #https://stackoverflow.com/questions/61507845/model-clean-vs-model-clean-fields
    def clean(self):
        """
        Validate rules for multiple fields before save it
        https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
        https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.clean
        """
        super().clean()
        self._number_plate_user_validator()
        self._car_user_validator()
        
        
    def __str__(self):
        return '{} {} {}'.format(self.car, self.user, self.number_plate)