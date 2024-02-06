from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from utils.django.models import get_user_model

User = get_user_model()

#https://docs.djangoproject.com/en/3.2/ref/validators/
def user_is_active_validator(value):
    value = User.objects.get(pk=value)
    
    if not value.is_active:
        raise ValidationError(_('%(value)s user is not active'),
                                params={'value': value},
                            )
        
