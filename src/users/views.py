from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import GroupSerializer, UserSerializer

from .filters import User_Filter

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = User_Filter
    queryset = User.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ['name']