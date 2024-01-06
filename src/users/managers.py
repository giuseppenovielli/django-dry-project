from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from django.db.models import Q, OuterRef, Subquery, Max, Count

from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    
    def email(self, email):
        """
        Get records with email
        """
        return self.filter(email=email)
    
    
    def username(self, username):
        """
        Get records with username
        """
        return self.filter(username=username)
    
    
    def first_name(self, first_name):
        """
        Get records with first_name
        """
        return self.filter(first_name=first_name)
    
    
    def last_name(self, last_name):
        """
        Get records with last_name
        """
        return self.filter(last_name=last_name)
    
    
    def is_active(self, is_active):
        """
        Get records with is_active
        """
        return self.filter(is_active=is_active)
    

    #motorizations
    def car_user(self):
        """
        Get records in motorizations,Car_user
        """
        from motorizations.models import Car_user
        
        return self.filter(id__in=Subquery(
                Car_user.objects.values('user_id')
            )
        )
        
    
    def number_plate__contains(self, number_plate):
        """
        Get records in motorizations, Car_user whitch contains number_plate
        """
        from motorizations.models import Car_user
        
        return self.filter(id__in=Subquery(
                Car_user.objects.number_plate__contains(number_plate).values('user_id')
            )
        )