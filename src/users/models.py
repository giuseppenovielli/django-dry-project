from django.contrib.auth.models import AbstractUser

from .managers import User_QuerySet, UserManager

class User(AbstractUser):
    
    def __str__(self):
        return self.email
    
    #ISSUE NOT DRY -> https://stackoverflow.com/questions/59524378/add-queryset-as-manager-to-the-abstractuser-model
    #UserManager inheritance from BaseUserManager (django package) a it is a models.Manager
    #models.Manager NOT DRY WHEN ADD CUSTOM QUERIES (DUPLICATE SAME METHODS) -> https://docs.djangoproject.com/en/3.2/topics/db/managers/#calling-custom-queryset-methods-from-the-manager 
    
    objects = UserManager()