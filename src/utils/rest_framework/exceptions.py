from django.core.exceptions import ValidationError

from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler
from rest_framework.response import Response

#https://github.com/encode/django-rest-framework/discussions/7850#discussioncomment-1855682
def django_error_handler(exc, context):
    """Handle django core's errors."""
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is None and isinstance(exc, ValidationError):
        response = Response(status=400, data=as_serializer_error(exc))
    return response