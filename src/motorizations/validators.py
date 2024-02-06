from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from utils.django.models import get_user_model

from .groups import CAR_USER_MANAGERS

User = get_user_model()

#https://docs.djangoproject.com/en/3.2/ref/validators/
def user_write_authorization_validator(value):
    value = User.objects.get(pk=value)
    
    if not value.groups.filter(name=CAR_USER_MANAGERS).exists():
        raise ValidationError(_('%(value)s user is not an authorized'),
                                params={'value': value},
                            )
        
