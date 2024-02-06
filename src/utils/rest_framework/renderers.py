from django.core.exceptions import PermissionDenied

from rest_framework import renderers

from django_dry.settings import DEBUG
    
    
class Debug_BrowsableAPIRenderer(renderers.BrowsableAPIRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context.get("request", None)
        if DEBUG:
            return super().render(data=data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)
        raise PermissionDenied