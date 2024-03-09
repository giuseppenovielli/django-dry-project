from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CustomAuthToken,
                    UserViewSet, GroupViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('api/', include((router.urls))),
    path('api-token-auth/', CustomAuthToken.as_view()),
]