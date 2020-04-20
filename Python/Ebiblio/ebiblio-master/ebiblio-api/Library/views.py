from DjangoLibraryRest.pagination import StandardResultsSetPagination
from Login.models import IsAdminOrReadListBookOnly, IsOwnerOrAdmin, \
    check_is_in, IsAdminOrOnlyRent
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_409_CONFLICT, \
    HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED, HTTP_404_NOT_FOUND

from .models import Book, History, rent_reserved_book, edit_loan_history, \
    check_if_valid_post_book, check_if_valid_put_book, ApiResults, \
    check_is_empty
from .serializers import BookSerializer, HistorySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminOrReadListBookOnly,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('uuid_book',
                       'isbn',
                       'available_book',
                       'deleted_book')
    ordering = ('deleted_book',)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.user.is_staff is False:
            queryset = queryset.exclude(deleted_book=True)

        if self.paginate_queryset(queryset) is not None \
                and self.request.query_params.get('page_size', False):

            serializer = self.get_serializer(self.paginate_queryset(queryset),
                                             many=True,
                                             context={'request': request})

        else:
            serializer = self.get_serializer(queryset, many=True,
                                             context={'request': request})

        if request.user.is_authenticated:
            for i in range(len(serializer.data)):
                book = Book.objects.get(
                    uuid_book=serializer.data[i]['uuid_book'])

                reserved_histories = History.objects.filter(book=book,
                                                            user=request.user,
                                                            returned_book=False)
                if len(reserved_histories) == 1:
                    serializer.data[i]['uuid_loan'] = reserved_histories[0].uuid_loan
                else:
                    serializer.data[i]['uuid_loan'] = None
        else:
            for i in range(len(serializer.data)):
                serializer.data[i]['uuid_loan'] = None

        if self.paginate_queryset(queryset) is not None \
                and self.request.query_params.get('page_size', False):
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.deleted_book is False or request.user.is_staff is True:

            serializer = self.get_serializer(instance=instance,
                                             context={'request': request})
            response = serializer.data

            status = HTTP_200_OK
        else:
            response = 'Not found'
            status = HTTP_404_NOT_FOUND
        return Response(response, status)

    def create(self, request, *args, **kwargs):
        try:
            book = check_if_valid_post_book(request)
            serializer = BookSerializer(instance=book,
                                        context={'request': request})
            status = HTTP_201_CREATED
            response = serializer.data
        except Exception as error:
            status = HTTP_409_CONFLICT
            response = error.args[0]

        return Response(response, status=status)

    def update(self, request, *args, **kwargs):
        try:

            book = check_if_valid_put_book(request, self.get_object())

            serializer = BookSerializer(instance=book,
                                        context={'request': request})
            status = HTTP_200_OK
            response = serializer.data

        except Exception as error:
            status = HTTP_409_CONFLICT
            response = error.args[0]

        return Response(response, status=status)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            instance.deleted_book = True
            instance.save()

            serializer = BookSerializer(instance=instance,
                                        context={'request': request})

            response = serializer.data
            status = HTTP_200_OK

        except:
            status = HTTP_404_NOT_FOUND
            response = 'NOT FOUND'

        return Response(response, status)


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminOrOnlyRent,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('uuid_loan',
                       'date_initial_loan',
                       'date_finished_loan',
                       'book',
                       'user',
                       'returned_book')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if self.paginate_queryset(queryset) is not None \
                and self.request.query_params.get('page_size', False):
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:

            user = User.objects.get(pk=request.data['pk'])
            book = Book.objects.get(uuid_book=request.data['uuid_book'])

            if check_is_in(request.data.get('reserved_book', False)):
                action = 'reserved'
            else:
                action = 'rent'

            history = rent_reserved_book(user, book, request.user, action)

            serializer = HistorySerializer(history,
                                           context={'request': request})
            status = HTTP_201_CREATED
            response = serializer.data

        except Exception as error:
            status = HTTP_409_CONFLICT
            response = error.args[0]

        return Response(response, status=status)

    def update(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=request.data['pk'])
            book = Book.objects.get(uuid_book=request.data['uuid_book'])

            request_history = self.get_object()

            if request_history.book != book or request_history.user != user:
                raise ValidationError('The data does not correspond')

            if check_is_in(request.data.get('renew_loan', False)) is True:

                history = edit_loan_history(request_history,
                                            request.user,
                                            'renew')

            elif check_is_in(request.data.get('renew_loan', False)) is False:

                history = edit_loan_history(request_history,
                                            request.user,
                                            'returned')

            else:
                raise ValidationError('Request params not valid')

            serializer = HistorySerializer(instance=history,
                                           context={'request': request})

            status = HTTP_200_OK

            response = serializer.data

        except Exception as error:
            status = HTTP_409_CONFLICT
            if len(error.args) != 0:
                response = error.args[0]
            else:
                response = error

        return Response(response, status=status)

    def destroy(self, request, *args, **kwargs):
        status = HTTP_405_METHOD_NOT_ALLOWED
        response = {"detail": "Method \"DELETE\" not allowed."}

        return Response(response, status=status)


@api_view(['GET'])
@permission_classes((IsOwnerOrAdmin,))
def get_user_history(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        history = History.objects.filter(user=user)
        status = HTTP_200_OK
        response = HistorySerializer(history, many=True,
                                     context={'request': request}).data

    except Exception as error:
        status = HTTP_404_NOT_FOUND
        response = "Not found."

    return Response(response, status=status)


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def get_book_history(request, uuid_book):
    try:
        book = Book.objects.get(uuid_book=uuid_book)
        history = History.objects.filter(book=book)
        status = HTTP_200_OK
        response = HistorySerializer(history, many=True,
                                     context={'request': request}).data
    except:
        status = HTTP_404_NOT_FOUND
        response = "Not found."
    return Response(response, status=status)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def find_in_google_api(request):
    try:
        data_to_check = {
            'isbn': request.data.get('isbn', 'Not found')
        }

        check_is_empty(data_to_check)
        data = ApiResults(data_to_check['isbn'])

        # response = {
        #     'title': data.data_book['Title'],
        #     'description': data.data_book['Desc'],
        #     'author': data.data_book['Authors'],
        #     'editorial': data.data_book['Publisher'],
        #     'language': data.data_book['Language']
        # }

        response = data.data_book

        status = HTTP_200_OK

    except Exception as error:
        response = error.args[0]
        if '403' in response:
            response = 'Something has happened, please enter the data manually.'
        status = HTTP_409_CONFLICT

    return Response(response, status=status)
