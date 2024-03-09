
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (EngineViewSet, CarViewSet, CarUserViewSet)

#https://blog.logrocket.com/django-rest-framework-create-api/#creating-api-views-django

router = DefaultRouter()
router.register(r'engines', EngineViewSet)
router.register(r'cars', CarViewSet)
router.register(r'cars-users', CarUserViewSet)

urlpatterns = [
    path('api/', include((router.urls))),
]