from rest_framework import pagination

#https://stackoverflow.com/questions/44370252/django-rest-framework-how-to-turn-off-on-pagination-in-modelviewset
#The following version allows, unlike the one described in the forum, a dynamic pagination size defined by the client
class Client_PageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 10

    def get_page_size(self, request):
        if not self.page_size_query_param:
            return self.page_size
        
        page_size = int(request.query_params.get(self.page_size_query_param, self.page_size))
        if page_size > 0:
            return page_size
        