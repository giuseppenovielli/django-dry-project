"""django_dry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

common_router = routers.DefaultRouter()

from motorizations import views as motorizations_views
common_router.register(r'engines', motorizations_views.Engine_ViewSet)
common_router.register(r'cars', motorizations_views.Car_ViewSet)
common_router.register(r'cars_users', motorizations_views.Car_user_ViewSet)

from users import views as users_views
common_router.register(r'users', users_views.UserViewSet)
common_router.register(r'groups', users_views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(common_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]