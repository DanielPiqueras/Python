from math import ceil
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        pages = ceil(self.page.paginator.count / int(
            self.request.query_params.get('page_size', 10)))

        return Response({'next': self.get_next_link(),
                         'previous': self.get_previous_link(),
                         'count': self.page.paginator.count,
                         'pages': pages,
                         'results': data})
