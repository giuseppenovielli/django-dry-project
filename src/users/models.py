from django.contrib.auth.models import AbstractUser

from .managers import UserManager

class User(AbstractUser):
    
    def __str__(self):
        return self.email
        
    objects = UserManager()
