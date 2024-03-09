from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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
    


class CustomAuthToken(ObtainAuthToken):
    """
    https://www.django-rest-framework.org/api-guide/authentication/#by-exposing-an-api-endpoint
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })