from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save)
def pre_save_full_clean_handler(sender, instance, *args, **kwargs):
    """ 
    Force all models to call full_clean before save 
    https://github.com/fish-ball/django-fullclean/blob/c0ac628f0b86fc8b8e4a7c0a63f25f2d70d29b4f/django_fullclean/__init__.py
    
    https://www.django-rest-framework.org/community/3.0-announcement/#differences-between-modelserializer-validation-and-modelform
    https://github.com/encode/django-rest-framework/discussions/7850#discussioncomment-8380135
    """
    from django.contrib.sessions.models import Session

    whitelist = getattr(settings, 'FULLCLEAN_WHITELIST', [''])
    allowed_by_whitelist = False
    
    for item in whitelist:
        if any([isinstance(item, list), isinstance(item, tuple)]):
            if sender.__module__.startswith(item[0]) and sender.__name__ == item[1]:
                allowed_by_whitelist = True
                break
        else:
            if sender.__module__.startswith(item):
                allowed_by_whitelist = True
                break

    if sender != Session and allowed_by_whitelist:
        print('pre_save_full_clean_handler: {}.full_clean()'.format(instance.__class__.__name__))
        instance.full_clean()