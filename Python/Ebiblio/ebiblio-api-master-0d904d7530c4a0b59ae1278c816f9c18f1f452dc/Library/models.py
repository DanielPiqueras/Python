import re
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta
from isbnlib import meta, desc, cover
from rest_framework.exceptions import ValidationError


class ApiResults(object):

    def __init__(self, isbn):
        self.data_book = meta(isbn)
        self.data_book['Desc'] = desc(isbn)
        self.data_book['Images'] = cover(isbn)


class Book(models.Model):
    uuid_book = models.UUIDField(primary_key=True, default=uuid.uuid4)
    isbn = models.TextField(max_length=50)

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    author = models.CharField(max_length=50)
    editorial = models.TextField()
    language = models.TextField()

    updated_user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                     related_name='updated_book')
    updated_time = models.DateTimeField(default=now)
    deleted_book = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=now)

    def edit_book(self, title, description, author, editorial, language, isbn,
                  user):
        self.title = title
        self.description = description
        self.author = author
        self.editorial = editorial
        self.language = language
        self.isbn = isbn
        self.updated_time = now()
        self.updated_user = user
        self.save()

    def __str__(self):
        return '%s' % self.isbn


class History(models.Model):
    uuid_loan = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_initial_loan = models.DateTimeField(default=now)
    date_finished_loan = models.DateTimeField(default=now)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reserved_book = models.BooleanField(default=False)
    returned_book = models.BooleanField(default=False)
    updated_user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                     related_name='updated_history')
    updated_time = models.DateTimeField(default=now)

    def __str__(self):
        return '{user} | {date_i} - {date_f} | Returned: {rented} | Reserved: {reserved}'.format(
            user=self.user,
            date_i=self.date_initial_loan,
            date_f=self.date_finished_loan,
            rented=self.returned_book,
            reserved=self.reserved_book
        )

    def create_loan(self, book, user, update_user):
        self.date_finished_loan = now() + timedelta(days=30)
        self.date_initial_loan = now()
        self.book = book
        self.user = user
        self.reserved_book = False
        self.updated_user = update_user
        self.save()

    def reserved(self, book, user, update_user):
        self.date_finished_loan = now() + timedelta(days=30)
        self.date_initial_loan = now()
        self.book = book
        self.user = user
        self.reserved_book = True
        self.updated_user = update_user
        self.save()

    def return_book(self, update_user):
        self.returned_book = True
        self.date_finished_loan = now()
        self.updated_user = update_user
        self.reserved_book = False
        self.updated_time = now()
        self.save()

    def renew_loan(self, update_user):
        self.returned_book = False
        self.date_finished_loan += timedelta(days=7)
        self.updated_user = update_user
        self.reserved_book = False
        self.updated_time = now()
        self.save()


def cont_books_rented_user(user):
    history = History.objects.filter(user=user, returned_book=False,
                                     reserved_book=False)

    return len(history)


def rent_reserved_book(user, book, updated_user, action):
    if cont_books_rented_user(user) >= 3:
        raise ValidationError(
            "The user already has three books rented at this time.")

    if action == 'rent':
        bad_history = History.objects.filter(book=book,
                                             returned_book=False,
                                             reserved_book=False)

        if len(bad_history) != 0:
            raise ValidationError('The book is already rent')

        bad_history = History.objects.filter(book=book,
                                             reserved_book=True).exclude(
            user=user)

        if len(bad_history) != 0:
            raise ValidationError('The book is already reserved by other user')
        history_reserved = History.objects.filter(book=book,
                                                  reserved_book=True,
                                                  returned_book=False,
                                                  user=user)
        if len(history_reserved) == 1:
            history = history_reserved[0]
        else:
            history = History()

        history.create_loan(book, user, updated_user)

    elif action == 'reserved':
        bad_history = History.objects.filter(book=book, reserved_book=True)

        if len(bad_history) != 0:
            raise ValidationError('The book is already reserved by other user')

        history = History()
        history.reserved(book, user, updated_user)

    response = history

    return response


def edit_loan_history(history, updated_user, action):
    if history.returned_book is True:
        raise ValidationError('The book has been returned')
    if action == 'returned':
        history.return_book(updated_user)
    elif action == 'renew':
        history.renew_loan(updated_user)
        histories_reserved = History.objects.filter(book=history.book,
                                                    reserved_book=True)

        if len(histories_reserved) != 0:
            for history_reserved in histories_reserved:
                history_reserved.date_finished_loan = history.date_finished_loan + timedelta(
                    days=30)
                history_reserved.save()
    response = history

    return response


def check_is_empty(attrs):
    for attribute in attrs:
        if attrs[attribute] == 'Not found':
            raise ValidationError(
                'The {data} has not been sent'.format(data=attribute))

        if isinstance(attrs[attribute], str) is False:
            raise ValidationError(
                'The {data} need to be string'.format(data=attribute))

        if len(attrs[attribute]) == 0:
            raise ValidationError(
                'The {data} is empty'.format(data=attribute))

        if attribute == 'isbn':
            if attrs[attribute][0] == ' ':
                raise ValidationError(
                    'Can not start or only contain whitespace')
            elif not validate_isbn(attrs[attribute]):
                raise ValidationError("Invalid ISBN")
        elif attrs[attribute][0] == ' ':
            raise ValidationError(
                'Can not start or only contain whitespace')

    return True


def validate_isbn(isbn):
    if len(isbn.replace("-", "").replace(" ", "").upper()) == 10:
        isbn = isbn.replace("-", "").replace(" ", "").upper()
        match = re.search(r'^(\d{9})(\d|X)$', isbn)
        if not match:
            return False

        digits = match.group(1)
        check_digit = 10 if match.group(2) == 'X' else int(match.group(2))

        result = sum((i + 1) * int(digit) for i, digit in enumerate(digits))
        return (result % 11) == check_digit

    elif len(isbn.replace("-", "").replace(" ", "").upper()) == 13 \
            and len(re.findall(r'\d', isbn)) == 13:
        d = re.findall(r'\d', isbn)
        last = d.pop()
        val = sum((x % 2 * 2 + 1) * int(y) for x, y in enumerate(d))
        check = 10 - (val % 10)
        if check == 10:
            check = "0"
        return str(check) == last
    else:
        return False


def check_if_valid_post_book(request):
    data_to_check = {
        'isbn': request.data.get('isbn', 'Not found'),
        'title': request.data.get('title', 'Not found'),
        'author': request.data.get('author', 'Not found'),
        'editorial': request.data.get('editorial', 'Not found'),
        'language': request.data.get('language', 'Not found')
    }
    check_is_empty(data_to_check)

    book = Book()

    description = request.data.get('description', '')

    if description is None:
        description = ''
    elif not isinstance(description, str):
        raise ValidationError('The description must be string')

    book.edit_book(
        str(request.data['title']),
        str(description),
        str(request.data['author']),
        str(request.data['editorial']),
        str(request.data['language']),
        str(request.data['isbn']),
        request.user
    )

    return book


def check_if_valid_put_book(request, book):
    data_to_check = {
        'isbn': request.data.get('isbn', 'Not found'),
        'title': request.data.get('title', 'Not found'),
        'author': request.data.get('author', 'Not found'),
        'editorial': request.data.get('editorial', 'Not found'),
        'language': request.data.get('language', 'Not found')
    }

    check_is_empty(data_to_check)

    description = request.data.get('description', '')

    if description is None:
        description = ''
    elif not isinstance(description, str):
        raise ValidationError('The description must be string')

    book.edit_book(
        str(request.data['title']),
        str(description),
        str(request.data['author']),
        str(request.data['editorial']),
        str(request.data['language']),
        str(request.data['isbn']),
        request.user
    )

    book.save()

    return book
