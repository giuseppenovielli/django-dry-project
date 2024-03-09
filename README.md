# Django DRY Project
A Django project with samples code strictly DRY (DON'T REPEAT YOURSELF)

## Features
### CRUD (Create Retrieve Update Delete)
CRUD are operations that most project implements.
[Django Rest Framework](https://www.django-rest-framework.org/) can be used for this purpose, to develop Rest API Endpoint.

+ #### API with a Model
  + [viewsets.ModelViewSet](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/motorizations/views.py#L19) Use this class if you want enable to consume all CRUD operations
  + [viewsets.GenericViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#custom-viewset-base-classes) Use these classes to enable only some CRUD operations.
 
+ #### API without a Model
  + [viewsets.ViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions) Use this class if you want enable to consume all CRUD operations
    
+ #### API with ExtraActions
  + [decorators.action](https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing)
    
+ #### RETRIEVE
  + Simple queries
    + [Search](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/users/views.py#L30)
  + Advanced queries
    + [Django Filter](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/motorizations/filters.py)
    + [Manager Query Engine (Experimental)](https://github.com/giuseppenovielli/django_dry_project/wiki/Manger-Query-Engine-%5BExperimental%5D)

+ #### CREATE/UPDATE
  + Validations Model layer
    + Write Validations logic into [Model.clean()](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/motorizations/models.py#L102) that check model fields data integrity.
    If call Model.save() from Model.Form, Model.Serializer, ModelAdmin object MUST BE validated before saved into db.
    + Warnings
      + [pre_save_full_clean_handler](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/utils/django/signals.py#L7) model.full_clean() is not called by default when invoke Model.save() method [ISSUE](https://stackoverflow.com/questions/4441539/why-doesnt-djangos-model-save-call-full-clean)
      + [django_error_handler](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/utils/rest_framework/exceptions.py#L8C5-L8C25) Improve conversion from exceptions.ValidationError() to serializer.ValidationError()
  + Validations View layer
    + Write Validations logic into [ModelSerializer.validate() and ModelForms.clean() YES NOT DRY 😅](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/motorizations/serializers.py#L51) that check model fields data integrity using view parameters as request, that aren't accessible into Model class.
  + Single row
    + [Model](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/motorizations/views.py#L69)
  + Nested ForeignKey
    + [Multiple Models](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/motorizations/views.py#L69)

+ #### UPDATE
  + Warnings
    + [UpdateModelQuerySet](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/motorizations/managers.py#L82) Add this Mixing for prevent update not call Model.save() method. [Unfortunately, there isn’t a workaround when creating or updating objects in bulk, since none of save(), pre_save, and post_save are called.](https://docs.djangoproject.com/en/3.2/topics/db/models/#overriding-predefined-model-methods)

+ #### DELETE
  + Validations Model layer
    + Write Validations logic into [signals.pre_delete](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/motorizations/signals.py#L10)
  + Validations View layer
    + Write Validations logic into [viewsets.destroy() YES NOT DRY 😅](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/motorizations/views.py#L73) that check model fields data integrity using view parameters as request, that aren't accessible into Model/Signal class.
---
### Utils
[Utils](https://github.com/giuseppenovielli/django_dry_project/tree/main/src/utils) folder can be used to store utils method/class
+ Create for each plugin, one utils file
---
### Pagination
[Client_PageNumberPagination](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/utils/rest_framework.py) class can be used to enable client custom pagination size.
+ `<url>?page_size=20` Get 20 items at time, get page=1 (default) 
+ `<url>?page=2` Get the page number, get page_size=10 (default)
+ `<url>?page_size=20&page=2` Get 20 items at time, get page=2
---
### BrowsableAPIRenderer DEBUG MODE ONLY 
[Debug_BrowsableAPIRenderer](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/utils/rest_framework.py#L23) class can be used to use browsable api ONLY into DEBUG MODE.
