from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        status = response.status_code

        if not isinstance(response.data, str) and len(response.data) != 0:

            if isinstance(response.data, dict):
                if response.data.get('detail', False):
                    response = response.data['detail']
            elif response is not None:
                status = response.data[0].code
                response = response.data[0]

    else:
        status = HTTP_500_INTERNAL_SERVER_ERROR

    return Response(response, status=status)
