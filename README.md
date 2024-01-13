# Django DRY Project
A Django project with samples code strictly DRY (DON'T REPEAT YOURSELF)

## Features
### CRUD (Create Retrieve Update Delete)
CRUD are operations that most project implements.
[Django Rest Framework](https://www.django-rest-framework.org/) can be used for this purpose, to develop Rest API Endpoint.
+ #### RETRIEVE
  + Simple queries
    + [Search](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/users/views.py#L30)
  + Advanced queries
    + [Django Filter](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/motorizations/filters.py)
    + [Manager Query Engine (Experimental)](https://github.com/giuseppenovielli/django_dry_project/wiki/Manger-Query-Engine-%5BExperimental%5D)

+ #### CREATE (TODO)
+ #### UPDATE (TODO)
+ #### DELETE (TODO)
---
### Utils
[Utils](https://github.com/giuseppenovielli/django_dry_project/tree/main/src/utils) folder can be used to store utils method/class
+ Create for each plugin utils file
---
### Pagination
[Client_PageNumberPagination](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/utils/rest_framework.py) class can be used to enable client custom pagination size.
+ `<url>?page_size=20` Get 20 items at time, get page=1 (default) 
+ `<url>?page=2` Get the page number, get page_size=10 (default)
+ `<url>?page_size=20&page=2` Get 20 items at time, get page=2
---
### BrowsableAPIRenderer DEBUG MODE ONLY 
[Debug_BrowsableAPIRenderer](https://github.com/giuseppenovielli/django_dry_project/blob/main/src/utils/rest_framework.py#L23) class can be used to use browsable api ONLY into DEBUG MODE.
