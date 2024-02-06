from django.apps import AppConfig


class MotorizationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'motorizations'
    
    #https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
    def ready(self):
        import motorizations.signals
