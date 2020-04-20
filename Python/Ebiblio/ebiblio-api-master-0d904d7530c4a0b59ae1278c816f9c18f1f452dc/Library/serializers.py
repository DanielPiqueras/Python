import json

from rest_framework import serializers

from Login.serializers import UserSerializer
from .models import History, Book, ApiResults


class BookSerializer(serializers.HyperlinkedModelSerializer):
    last_user = serializers.SerializerMethodField()
    available_book = serializers.SerializerMethodField()
    reserved_book = serializers.SerializerMethodField()

    class Meta:
        model = Book
        read_only_fields = ('uuid_book',)
        fields = (
            'uuid_book',
            'title',
            'description',
            'author',
            'editorial',
            'language',
            'isbn',
            'available_book',
            'last_user',
            'deleted_book',
            'reserved_book'
        )

    def get_available_book(self, instance):
        request = self.context.get('request')
        try:
            if len(History.objects.filter(book=instance,
                                          returned_book=False)) != 0:
                available = False
            else:
                available = True
        except:
            available = True

        return available

    def get_reserved_book(self, instance):
        request = self.context.get('request')
        try:
            if len(History.objects.filter(book=instance,
                                          reserved_book=True)) != 0:
                available = True
            else:
                available = False
        except:
            available = 'error'

        return available

    def get_last_user(self, instance):
        request = self.context.get('request')
        last_user = None
        if request is not None:
            user = request.user
            histories = History.objects.filter(book=instance,
                                               returned_book=False,
                                               reserved_book=False)
            if len(histories) == 1 and user.is_authenticated:
                last_user = histories[0].user.username
            else:
                last_user = None

        return last_user


class HistorySerializer(serializers.HyperlinkedModelSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = History
        read_only_fields = ('uuid_loan',)
        fields = (
            'uuid_loan',
            'date_initial_loan',
            'date_finished_loan',
            'book',
            'user',
            'returned_book',
            'reserved_book'
        )
