from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import signals
from django.dispatch import receiver

from .models import CarUser


@receiver(signals.pre_delete, sender=CarUser)
def car_user_pre_delete(sender, instance, **kwargs):
    """
    Write delete validation logic
    
    https://stackoverflow.com/questions/38794808/how-to-prevent-model-instance-deletion
    https://docs.djangoproject.com/en/3.2/topics/db/models/#overriding-predefined-model-methods
    
    get user_logged_in -> https://stackoverflow.com/questions/4721771/get-current-user-log-in-signal-in-django NOT ADVISED
    """
    return
    raise ValidationError(_('This object can\'t be deleted'))