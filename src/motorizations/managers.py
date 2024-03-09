from django.db import models
from django.db.models import Q, OuterRef, Subquery

from utils.django.managers import UpdateModelQuerySet


class EngineQuerySet(models.QuerySet):
    
    def name(self, name):
        """
        Get records with name
        """
        return self.filter(name=name)
    
    
    #Car_user
    def car__car_user__user(self, user):
        """
        Get records with user
        """
        from .models import Car
        
        return self.filter(id__in=Subquery(
                Car.objects.car_user__user(user).values('engine_id')
            )
        )
        
        
    def car__car_user__number_plate__contains(self, number_plate):
        """
        Get records with user
        """
        from .models import Car
        
        return self.filter(id__in=Subquery(
                Car.objects.car_user__number_plate__contains(number_plate).values('engine_id')
            )
        )
        
    
class CarQuerySet(models.QuerySet):
    
    def name(self, name):
        """
        Get records with name
        """
        return self.filter(name=name)
    
    
    def engine(self, engine):
        """
        Get records with engine
        """
        return self.filter(engine=engine)
    
    
    #Car_user
    def car_user__user(self, user):
        """
        Get records with user
        """
        from .models import Car_user
        
        return self.filter(id__in=Subquery(
                Car_user.objects.user(user).values('car_id')
            )
        )
        
        
    def car_user__number_plate__contains(self, number_plate):
        """
        Get records with number plate contains
        """
        from .models import Car_user
        
        return self.filter(id__in=Subquery(
                Car_user.objects.number_plate__contains(number_plate).values('car_id')
            )
        )
    
    
class CarUserQuerySet(UpdateModelQuerySet, models.QuerySet):
    
    #TABLE FIELDS
    def number_plate(self, number_plate):
        """
        Get records with number_plate
        """
        return self.filter(number_plate=number_plate)
    
    
    def number_plate__contains(self, number_plate):
        """
        Get records contains number_plate
        """
        return self.filter(number_plate__contains=number_plate)
    
    
    def car(self, car):
        """
        Get records with car
        """
        return self.filter(car=car)
    
    
    def user(self, user):
        """
        Get records with user
        """
        return self.filter(user=user)
    
    #
    
    #ACCESS TO RELATED FILEDS
    def car__engine(self, engine):
        """
        Get records with engine
        """
        from .models import Car
        
        return self.filter(car_id__in=Subquery(
                Car.objects.engine(engine).values('id')
            )
        )
        
        
    def user__email(self, email):
        """
        Get records with user__email
        """
        from users.models import User
        
        return self.filter(user_id__in=Subquery(
                User.objects.email(email).values('id')
            )
        )
        