from django.core.exceptions import PermissionDenied

from rest_framework import pagination, renderers

from django_dry.settings import DEBUG

#https://stackoverflow.com/questions/44370252/django-rest-framework-how-to-turn-off-on-pagination-in-modelviewset
#La versione seguente, consente, a differenza di quella descritta nel forum, una dimensione di paginazione dinamica definita dal client
class Client_PageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 10

    def get_page_size(self, request):
        if not self.page_size_query_param:
            return self.page_size
        
        page_size = int(request.query_params.get(self.page_size_query_param, self.page_size))
        if page_size > 0:
            return page_size
        
    
    
class Debug_BrowsableAPIRenderer(renderers.BrowsableAPIRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context.get("request", None)
        if DEBUG:
            return super().render(data=data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)
        raise PermissionDenied