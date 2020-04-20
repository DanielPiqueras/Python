import json
from unittest import mock
from unittest.mock import patch, Mock

from django.contrib.auth.models import User
from django.test import override_settings
from isbnlib import meta, desc, cover
from rest_framework import status
from rest_framework.test import APITestCase

from Library.serializers import BookSerializer, HistorySerializer
from .models import Book, History


# The tests do not use paging.

def log_in():
    admin = User.objects.create_superuser("admin", "", "admin")
    admin.save()


isbn9783161484100 = {'ISBN-13': '9783161484100',
                     'Title': 'An Essay Commissioned For The Exhibition: "Regarding Henry\'s Show" @ The Brant Foundation Art Study Center, Greenwich, CT, 2009',
                     'Authors': [''],
                     'Publisher': '',
                     'Year': '2009',
                     'Language': 'en',
                     'Desc': None,
                     'Images': {
                         'smallThumbnail': 'http://books.google.com/books/content?id=CtCLAwAAQBAJ&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api',
                         'thumbnail': 'http://books.google.com/books/content?id=CtCLAwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'
                     }
                     }

isbn9788467510881 = {'ISBN-13': '9788467510881', 'Title': 'Lobito, terror de los mares', 'Authors': ['Ian Whybrow'],
                     'Publisher': 'Ediciones Sm', 'Year': '2006', 'Language': 'es',
                     'Desc': 'El capitán Feroche navega a sus anchas por los siete mares. Pero el\nvaliente Lobito y sus intrépidos amigos han decidido buscar el tesoro de\neste feroz bucanero. ¿Será el comienzo de otra maravillosa aventura? Una\nhistoria en la que se entremezclan el humor, la amistad y las relaciones\nfamiliares.',
                     'Images': {
                         'smallThumbnail': 'http://books.google.com/books/content?id=do9vGQAACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api',
                         'thumbnail': 'http://books.google.com/books/content?id=do9vGQAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'
                     }
                     }

isbn0198526636 = {'ISBN-13': '9780198526636', 'Title': 'Taking Chances', 'Authors': ['John Haigh'],
                  'Publisher': 'Oxford University Press, USA', 'Year': '2003', 'Language': 'en',
                  'Desc': '"What are the odds against winning the Lotto, The Weakest Link, or Who\nWants to be a Millionaire? The answer lies in the science of probability,\nyet many of us are unaware of how this science works. Every day, people\nmake judgements on a wide variety of situations where chance plays a role,\nincluding buying insurance, betting on horse-racing, following medical\nadvice - even carrying an umbrella. In Taking Chances, John Haigh guides\nthe reader round common pitfalls, demonstrates how to make better-informed\ndecisions, and shows where the odds can be unexpectedly in your favour.\nThis new edition has been fully updated, and includes information on top\ntelevision shows, plus a new chapter on Probability for Lawyers."--BOOK\nJACKET.',
                  'Images': {
                      'smallThumbnail': 'http://books.google.com/books/content?id=11NxcwgqdJkC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api',
                      'thumbnail': 'http://books.google.com/books/content?id=11NxcwgqdJkC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'
                  }
                  }

isbn9780316029186 = {'ISBN-13': '9780316029186',
                     'Title': 'The Last Wish',
                     'Authors': ['Andrzej Sapkowski'],
                     'Publisher': 'Orbit',
                     'Year': '2008',
                     'Language': 'en',
                     'Desc': 'Geralt of Rivia is a witcher. A cunning sorcerer. A merciless assassin. And\na cold-blooded killer. His sole purpose: to destroy the monsters that\nplague the world. But not everything monstrous-looking is evil and not\neverything fair is good. . . and in every fairy tale there is a grain of\ntruth. The international hit that inspired the video game: The Witcher.',
                     'Images': {
                         'smallThumbnail': 'http://books.google.com/books/content?id=GkqdlwEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api',
                         'thumbnail': 'http://books.google.com/books/content?id=GkqdlwEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'
                     }
                     }

isbn842261586X = '9788422615866'

json_data = [isbn9783161484100, isbn9788467510881, isbn0198526636, isbn9780316029186]


def mock_book_data(self, i):
    isbn = self.valid_isbns[i]['isbn']
    isbn = isbn.replace(" ", "").replace("-", "")

    if isbn == "9788467510881":
        mock_data = isbn9788467510881
    elif isbn == "0198526636":
        mock_data = isbn0198526636
    elif isbn == "9780316029186":
        mock_data = isbn9780316029186
    elif isbn == "842261586X":
        mock_data = isbn842261586X
    else:
        mock_data = isbn9783161484100

    return mock_data


class GetAllBooksTest(APITestCase):
    global json_data

    def setUp(self):
        log_in()

        User.objects.create_user(username="Leandro", email="", password="0000")

        book1 = Book()
        book1.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                        editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                        isbn='978-3-16-148410-0', user=User.objects.get(username='admin'))

        book2 = Book()
        book2.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                        editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                        isbn='978-3-16-148410-0', user=User.objects.get(username='admin'))

        book3 = Book()
        book3.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                        editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                        isbn='978-3-16-148410-0',
                        user=User.objects.get(username='admin'))

        book4 = Book()
        book4.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                        editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                        isbn='978-3-16-148410-0',
                        user=User.objects.get(username='admin'))

        book4.deleted_book = True
        book4.save()

    def test_get_all_books_admin(self):
        print("#########-Test GET books Admin-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/books/")
        # print(response.data)  # Debug
        # get data from db
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        # Temporary treatment to check the rest of the data.
        for i in range(len(response.data)):
            response.data[i]['last_user'] = None
            del response.data[i]['uuid_loan']

        self.assertEqual(response.data,  # ['data']
                         serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_books_NoStaff(self):
        print("#########-Test GET books NoStaff-#########")
        self.assertTrue(self.client.login(username='Leandro', password='0000'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/books/")
        # print(response.data)  # Debug
        # get data from db
        books = Book.objects.all().exclude(deleted_book=True)
        serializer = BookSerializer(books, many=True)

        # Temporary treatment to check the rest of the data.
        for i in range(len(response.data)):
            response.data[i]['last_user'] = None
            del response.data[i]['uuid_loan']

        # print(">>>", response.data)     # Debug
        # print(">>>", serializer.data)   # Debug

        self.assertEqual(response.data,  # ['data']
                         serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_books_UnLogged(self):
        print("#########-Test GET books UnLogged-#########")

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/books/")
        # print(response.data)  # Debug
        # get data from db
        books = Book.objects.all().exclude(deleted_book=True)
        serializer = BookSerializer(books, many=True)

        # Check if last_user is hidden.
        for i in range(len(response.data)):
            self.assertEqual(response.data[i]['last_user'], None)
            self.assertEqual(response.data[i]['uuid_loan'], None)
            del response.data[i]['uuid_loan']

        # print(">>>", response.data)     # Debug
        # print(">>>", serializer.data)   # Debug

        self.assertEqual(response.data,  # ['data']
                         serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetBookTest(APITestCase):
    uuid = "None"
    global json_data

    def setUp(self):
        log_in()

        book = Book()
        book.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                       editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                       isbn='978-3-16-148410-0',
                       user=User.objects.get(username='admin'))

        self.uuid = book.uuid_book

        self.book_rented = Book()
        self.book_rented.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                                   editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                                   isbn='978-3-16-148410-0',
                                   user=User.objects.get(username='admin'))
        self.book_rented.save()

        self.user = User.objects.create_user(username="user1", email="", password="user1")

        self.client.login(username="admin", password="admin")

        # Rent Book
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book_rented.uuid_book),
                                        'pk': self.user.pk,
                                        'renew_loan': False
                                    }),
                                    content_type='application/json')

        # print(">>>ugfs>", response.data)    # Debug

        self.history = History.objects.get(user=self.user, book=self.book_rented)

        self.client.logout()

    def test_get_book_valid(self):
        print("#########-Test GET Book exists-#########")

        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/books/{}/".format(self.uuid))
        # print(response.data)  # Debug
        # get data from db
        book = Book.objects.get(uuid_book=self.uuid)
        serializer = BookSerializer(book)

        # Temporary treatment to check the rest of the data.
        response.data['last_user'] = None

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_book_valid_lastUser(self):
        print("#########-Test GET Book Last_User-#########")

        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/books/{}/".format(self.book_rented.uuid_book))
        # print(response.data)  # Debug

        self.assertEqual(response.data['last_user'], self.history.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_book_invalid(self):
        print("#########-Test GET Book no exists-#########")
        # log_in()
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/books/0378a1e7-25f8-4d39-b457-374770620d11/")
        # print(response.status_code)  # Debug
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ValidPostBookTest(APITestCase):
    global json_data

    def setUp(self):
        self.user = User.objects.create_user(username="user1",
                                             email="",
                                             password="user1")
        self.user.save()

        # Valid
        self.valid_book0 = {
            'title': "Test 1 - Lobito",
            'uuid_book': "something-random",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-84-675-1088-1"
        }
        self.valid_book1_WithUUID_book = {
            'title': "Test 2",
            'uuid_book': "1234",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.valid_book2_emptyDescription = {
            'title': "Test 3",
            'uuid_book': "1234",
            'description': "",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.valid_book3_emptyUUID_Book = {
            'title': "Test 4",
            'uuid_book': "",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }

        self.valid_book4_noUUID_Book = {
            'title': "Test 5",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.valid_book5_noDescription = {
            'title': "Test 7",
            'uuid_book': "something",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.valid_book6_NoneDescription = {
            'title': "Test 8",
            'uuid_book': "something",
            'description': None,
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.valid_book7_ISBNSpace = {
            'title': "ISBNSpace_2",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978 3 16 148410 0"
        }
        self.valid_book8_ISBN10_X = {
            'title': "ISBN10 con X",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "842261586X"
        }

        self.valid_books = [self.valid_book0,
                            self.valid_book1_WithUUID_book,
                            self.valid_book2_emptyDescription,
                            self.valid_book3_emptyUUID_Book,
                            self.valid_book4_noUUID_Book,
                            self.valid_book5_noDescription,
                            self.valid_book6_NoneDescription,
                            self.valid_book7_ISBNSpace,
                            self.valid_book8_ISBN10_X]

    def test_create_valid_book(self):
        print("#########-Test POST Valid Book-#########")
        response = []
        log_in()
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response_get = self.client.get("http://127.0.0.1:8000/library/books/")
        # print(response_get.data)  # Debug
        # get data from db
        books = Book.objects.all()
        serializer_before = BookSerializer(books, many=True)
        self.assertEqual(response_get.data,  # ['data']
                         serializer_before.data)

        for i in range(len(self.valid_books)):
            response.append(self.client.post("http://127.0.0.1:8000/library/books/",
                                             data=json.dumps(self.valid_books[i]),
                                             content_type='application/json'))

            # print(">>", i, response[i].data)  # Debug

            self.assertEqual(response[i].status_code, status.HTTP_201_CREATED)

            # get data from db
            books = Book.objects.all()
            serializer_after = BookSerializer(books, many=True)
            self.assertNotEqual(serializer_before.data, serializer_after.data)

    def test_create_book_unLogged(self):
        print("#########-Test POST Book UnLogged-#########")
        response = self.client.post("http://127.0.0.1:8000/library/books/",
                                    data=json.dumps({
                                        'title': "Test 1 - Lobito",
                                        'uuid_book': "something-random",
                                        'description': "This is a test",
                                        'author': "Leandrous",
                                        'editorial': "Sewania",
                                        'language': "English",
                                        'isbn': "978-84-675-1088-1"
                                    }),
                                    content_type='application/json')

        # print(response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_noStaff(self):
        print("#########-Test POST Book noStaff-#########")
        self.assertTrue(self.client.login(username='user1', password='user1'))
        self.assertFalse(self.user.is_staff)

        response = self.client.post("http://127.0.0.1:8000/library/books/",
                                    data=json.dumps({
                                        'title': "Test 1 - Lobito",
                                        'uuid_book': "something-random",
                                        'description': "This is a test",
                                        'author': "Leandrous",
                                        'editorial': "Sewania",
                                        'language': "English",
                                        'isbn': "978-84-675-1088-1"
                                    }),
                                    content_type='application/json')

        # print(response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class InvalidPostBookTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1",
                                             email="",
                                             password="user1")
        self.user.save()

        # Invalids
        self.invalid_book0_emptyTitle = {
            'title': "",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book1_noTitle = {
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book2_NoneTitle = {
            'title': None,
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book3_NumberTitle = {
            'title': 0,
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book4_ListTitle = {
            'title': [0, "Title"],
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book5_TitleSpace = {
            'title': " WithSpace",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book6_NumberDescription = {
            'title': "Title",
            'uuid_book': "something",
            'description': 1278468,
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book7_ListDescription = {
            'title': "Title",
            'uuid_book': "something",
            'description': [0, "Description"],
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book8_emptyAuthor = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book9_noAuthor = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book10_NoneAuthor = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': None,
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book11_NumberAuthor = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': 0,
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book12_ListAuthor = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': [0, "author"],
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book13_AuthorSpace = {
            'title': "AuthorSpace",
            'uuid_book': "something",
            'description': "This is a test",
            'author': " Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book14_emptyEditorial = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book15_noEditorial = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book16_NoneEditorial = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': None,
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book17_NumberEditorial = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': 0,
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book18_ListEditorial = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': [0, "editorial"],
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book19_EditoSpace = {
            'title': "EditoSpace",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': " Sewania",
            'language': "English",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book20_emptyLanguage = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book21_noLanguage = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book22_NoneLanguage = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': None,
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book23_NumberLanguage = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': 0,
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book24_ListLanguage = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': [0, "language"],
            'isbn': "978-3-16-148410-0"
        }
        self.invalid_book25_LangSpace = {
            'title': "LangSpace",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': " English",
            'isbn': "978-3-16-148410-0"
        }

        self.invalid_book26_emptyISBN = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': ""
        }
        self.invalid_book27_noISBN = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English"
        }
        self.invalid_book28_NoneISBN = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': None
        }
        self.invalid_book29_ISBNSpace = {
            'title': "ISBNSpace_1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': " 978-3-16-148410-0"
        }
        self.invalid_book30_NumberISBN = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': 0
        }
        self.invalid_book31_ListISBN = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': [0, "12454"]
        }
        self.invalid_book32_OddISBN13_1 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '978-3-16-148410-0Avismal'
        }
        self.invalid_book33_OddISBN10_1 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '0198526636Avismal'
        }
        self.invalid_book34_OddISBN13_2 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '978-3-16-148410-0-Salt0AlVaci0'
        }
        self.invalid_book35_OddISBN10_2 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '0198526636-Salt0AlVaci0'
        }
        self.invalid_book36_OddISBN13_3 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '978-3-16-148410-Z'
        }
        self.invalid_book37_OddISBN10_3 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '019852663Z'
        }
        self.invalid_book38_OddISBN13_4 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '978-3-16-148410-0123762'
        }
        self.invalid_book39_OddISBN10_4 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '0198526636-01234'
        }
        self.invalid_book40_OddISBN13_5 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '978-3-16-148410-00000'
        }
        self.invalid_book41_OddISBN10_5 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '0198526636-0000'
        }
        self.invalid_book42_OddISBN10_6 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '842261586A'
        }

        self.invalid_books = [self.invalid_book0_emptyTitle,
                              self.invalid_book1_noTitle,
                              self.invalid_book2_NoneTitle,
                              self.invalid_book3_NumberTitle,
                              self.invalid_book4_ListTitle,
                              self.invalid_book5_TitleSpace,
                              self.invalid_book6_NumberDescription,
                              self.invalid_book7_ListDescription,
                              self.invalid_book8_emptyAuthor,
                              self.invalid_book9_noAuthor,
                              self.invalid_book10_NoneAuthor,
                              self.invalid_book11_NumberAuthor,
                              self.invalid_book12_ListAuthor,
                              self.invalid_book13_AuthorSpace,
                              self.invalid_book14_emptyEditorial,
                              self.invalid_book15_noEditorial,
                              self.invalid_book16_NoneEditorial,
                              self.invalid_book17_NumberEditorial,
                              self.invalid_book18_ListEditorial,
                              self.invalid_book19_EditoSpace,
                              self.invalid_book20_emptyLanguage,
                              self.invalid_book21_noLanguage,
                              self.invalid_book22_NoneLanguage,
                              self.invalid_book23_NumberLanguage,
                              self.invalid_book24_ListLanguage,
                              self.invalid_book25_LangSpace,
                              self.invalid_book26_emptyISBN,
                              self.invalid_book27_noISBN,
                              self.invalid_book28_NoneISBN,
                              self.invalid_book29_ISBNSpace,
                              self.invalid_book30_NumberISBN,
                              self.invalid_book31_ListISBN,
                              self.invalid_book32_OddISBN13_1,
                              self.invalid_book33_OddISBN10_1,
                              self.invalid_book34_OddISBN13_2,
                              self.invalid_book35_OddISBN10_2,
                              self.invalid_book36_OddISBN13_3,
                              self.invalid_book37_OddISBN10_3,
                              self.invalid_book38_OddISBN13_4,
                              self.invalid_book39_OddISBN10_4,
                              self.invalid_book40_OddISBN13_5,
                              self.invalid_book41_OddISBN10_5,
                              self.invalid_book42_OddISBN10_6]

    def test_create_invalid_book(self):
        print("#########-Test POST Invalid Book-#########")
        response = []
        log_in()

        for i in range(len(self.invalid_books)):
            self.assertTrue(self.client.login(username='admin', password='admin'))

            response.append(self.client.post("http://127.0.0.1:8000/library/books/",
                                             data=json.dumps(self.invalid_books[i]),
                                             content_type='application/json'))

            # print(">>", i, response[i].data)  # Debug

            self.assertEqual(response[i].status_code, status.HTTP_409_CONFLICT)


class ValidPutBookTest(APITestCase):
    global json_data

    def setUp(self):
        self.user = User.objects.create_user(username="user1",
                                             email="",
                                             password="user1")
        self.user.save()

        self.book = Book()
        self.book.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                            editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                            isbn="978-3-16-148410-0",
                            user=self.user)
        self.book.save()

        # Valid
        self.valid_put0 = {
            'title': "Test 1 - Lobito",
            'uuid_book': "something-random",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "978-84-675-1088-1"
        }
        self.valid_put1_WithUUID_book = {
            'title': "Test 2",
            'uuid_book': "1234",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.valid_put2_emptyDescription = {
            'title': "Test 3",
            'uuid_book': "1234",
            'description': "",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.valid_put3_emptyUUID_Book = {
            'title': "Test 4",
            'uuid_book': "",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.valid_put4_noUUID_Book = {
            'title': "Test 5",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.valid_put5_noDescription = {
            'title': "Test 7",
            'uuid_book': "something",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.valid_put6_NoneDescription = {
            'title': "Test 8",
            'uuid_book': "something",
            'description': None,
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.valid_put7_numberUUID_Book = {
            'title': "Test 4",
            'uuid_book': 2326454545654,
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.valid_put8_ISBNSpace_2 = {
            'title': "ISBNSpace",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0 19 852663 6"
        }

        self.valid_books = [self.valid_put0,
                            self.valid_put1_WithUUID_book,
                            self.valid_put2_emptyDescription,
                            self.valid_put3_emptyUUID_Book,
                            self.valid_put4_noUUID_Book,
                            self.valid_put5_noDescription,
                            self.valid_put6_NoneDescription,
                            self.valid_put7_numberUUID_Book,
                            self.valid_put8_ISBNSpace_2]

    def test_valid_update_book(self):
        print("#########-Test Valid PUT Admin-#########")
        response = []
        log_in()

        self.assertTrue(self.client.login(username='admin', password='admin'))
        uuid_book = self.book.uuid_book

        # get API response
        response_get = self.client.get("http://127.0.0.1:8000/library/books/")
        # print(response_get.data)  # Debug
        # get data from db
        books = Book.objects.all()

        # Temporary treatment to check the rest of the data.
        for i in range(len(response_get.data)):
            response_get.data[i]['last_user'] = None
            del response_get.data[i]['uuid_loan']

        serializer_before = BookSerializer(books, many=True)
        self.assertEqual(response_get.data,  # ['data']
                         serializer_before.data)

        # Put new data
        for i in range(len(self.valid_books)):
            response.append(self.client.put("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                            .format(uuid_book=uuid_book),
                                            data=json.dumps(self.valid_books[i]),
                                            content_type='application/json'))

            # print(">>", i, response[i].data)  # Debug
            self.assertEqual(response[i].status_code, status.HTTP_200_OK)

            # get data from db
            book_updated = Book.objects.get(uuid_book=uuid_book)
            serializer_b_updated = BookSerializer(book_updated)

            # Temporary treatment to check the rest of the data.
            response[i].data['last_user'] = None

            self.assertEqual(response[i].data['isbn'], serializer_b_updated.data['isbn'])  # ['data']
            books_updated = Book.objects.all()
            serializer_after = BookSerializer(books_updated, many=True)
            # compare changes:
            self.assertNotEqual(serializer_after.data, serializer_before.data)

    def test_cannot_delete_book_in_put(self):
        print("#########-Test Delete Book PUT-#########")
        log_in()

        self.assertTrue(self.client.login(username='admin', password='admin'))
        uuid_book = self.book.uuid_book

        response = self.client.put("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                   .format(uuid_book=uuid_book),
                                   data=json.dumps({
                                       'title': "NoDelete",
                                       'uuid_book': "something",
                                       'description': "This is a test",
                                       'author': "Leandrous",
                                       'editorial': "Sewania",
                                       'language': "English",
                                       'isbn': "0-19-852663-6",
                                       'deleted_book': True
                                   }),
                                   content_type='application/json')

        self.client.logout()

        response = self.client.get("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                   .format(uuid_book=uuid_book))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InvalidPutBookTest(APITestCase):
    global json_data

    def setUp(self):
        self.user = User.objects.create_user(username="user1",
                                             email="",
                                             password="user1")
        self.user.save()

        self.book = Book()
        self.book.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                            editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                            isbn="978-3-16-148410-0",
                            user=self.user)
        self.book.save()

        # Invalids
        self.invalid_put0_emptyTitle = {
            'title': "",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put1_noTitle = {
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put2_NoneTitle = {
            'title': None,
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put3_emptyAuthor = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put4_noAuthor = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put5_NoneAuthor = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': None,
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put6_emptyEditorial = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put7_noEditorial = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put8_NoneEditorial = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': None,
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put9_emptyLanguage = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put10_noLanguage = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put11_NoneLanguage = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': None,
            'isbn': "0-19-852663-6"
        }
        self.invalid_put12_emptyISBN = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': ""
        }
        self.invalid_put13_noISBN = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English"
        }
        self.invalid_put14_NoneISBN = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': None
        }
        self.invalid_put15_NumberTitle = {
            'title': 0,
            'uuid_book': "algo-random",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put17_NumberDescription = {
            'title': "Number",
            'uuid_book': "algo-random",
            'description': 0,
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put16_NumberAuthor = {
            'title': "Number",
            'uuid_book': "algo-random",
            'description': "This is a test",
            'author': 0,
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put18_NumberEditorial = {
            'title': "Number",
            'uuid_book': "algo-random",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': 0,
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put19_NumberLanguage = {
            'title': "Number",
            'uuid_book': "algo-random",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': 0,
            'isbn': "0-19-852663-6"
        }
        self.invalid_put20_NumberISBN = {
            'title': "Number",
            'uuid_book': "algo-random",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': 9783161484100
        }
        self.invalid_put21_TitleSpace = {
            'title': " WithSpace",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put22_AuthorSpace = {
            'title': "AuthorSpace",
            'uuid_book': "something",
            'description': "This is a test",
            'author': " Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put23_EditoSpace = {
            'title': "EditoSpace",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': " Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put24_LangSpace = {
            'title': "LangSpace",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': " English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put25_ISBNSpace = {
            'title': "ISBNrSpace",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': " 0-19-852663-6"
        }
        self.invalid_put26_ListTitle = {
            'title': [0, "title"],
            'uuid_book': "algo-random",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put27_ListDescription = {
            'title': "Number",
            'uuid_book': "algo-random",
            'description': [0, "description"],
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put28_ListAuthor = {
            'title': "Number",
            'uuid_book': "algo-random",
            'description': "This is a test",
            'author': [0, "author"],
            'editorial': "Sewania",
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put29_ListEditorial = {
            'title': "Number",
            'uuid_book': "algo-random",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': [0, "editorial"],
            'language': "English",
            'isbn': "0-19-852663-6"
        }
        self.invalid_put30_ListLanguage = {
            'title': "Number",
            'uuid_book': "algo-random",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': [0, "language"],
            'isbn': "0-19-852663-6"
        }
        self.invalid_put31_ListISBN = {
            'title': "Number",
            'uuid_book': "algo-random",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': [9783161484100, "isbn"]
        }
        self.invalid_put32_OddISBN13_1 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '978-3-16-148410-0Avismal'
        }
        self.invalid_put33_OddISBN10_1 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '0198526636Avismal'
        }
        self.invalid_put34_OddISBN13_2 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '978-3-16-148410-0-Salt0AlVaci0'
        }
        self.invalid_put35_OddISBN10_2 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '0198526636-Salt0AlVaci0'
        }
        self.invalid_put36_OddISBN13_3 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '978-3-16-148410-Z'
        }
        self.invalid_put37_OddISBN10_3 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '019852663Z'
        }
        self.invalid_put38_OddISBN13_4 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '978-3-16-148410-0123762'
        }
        self.invalid_put39_OddISBN10_4 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '0198526636-01234'
        }
        self.invalid_put40_OddISBN13_5 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '978-3-16-148410-00000'
        }
        self.invalid_put41_OddISBN10_5 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '0198526636-0000'
        }
        self.invalid_put42_OddISBN10_6 = {
            'title': "TestInvalidBook1",
            'uuid_book': "something",
            'description': "This is a test",
            'author': "Leandrous",
            'editorial': "Sewania",
            'language': "English",
            'isbn': '842261586A'
        }

        self.invalid_books = [self.invalid_put0_emptyTitle,
                              self.invalid_put1_noTitle,
                              self.invalid_put2_NoneTitle,
                              self.invalid_put3_emptyAuthor,
                              self.invalid_put4_noAuthor,
                              self.invalid_put5_NoneAuthor,
                              self.invalid_put6_emptyEditorial,
                              self.invalid_put7_noEditorial,
                              self.invalid_put8_NoneEditorial,
                              self.invalid_put9_emptyLanguage,
                              self.invalid_put10_noLanguage,
                              self.invalid_put11_NoneLanguage,
                              self.invalid_put12_emptyISBN,
                              self.invalid_put13_noISBN,
                              self.invalid_put14_NoneISBN,
                              self.invalid_put15_NumberTitle,
                              self.invalid_put16_NumberAuthor,
                              self.invalid_put17_NumberDescription,
                              self.invalid_put18_NumberEditorial,
                              self.invalid_put19_NumberLanguage,
                              self.invalid_put20_NumberISBN,
                              self.invalid_put21_TitleSpace,
                              self.invalid_put22_AuthorSpace,
                              self.invalid_put23_EditoSpace,
                              self.invalid_put24_LangSpace,
                              self.invalid_put25_ISBNSpace,
                              self.invalid_put26_ListTitle,
                              self.invalid_put27_ListDescription,
                              self.invalid_put28_ListAuthor,
                              self.invalid_put29_ListEditorial,
                              self.invalid_put30_ListLanguage,
                              self.invalid_put31_ListISBN,
                              self.invalid_put32_OddISBN13_1,
                              self.invalid_put33_OddISBN10_1,
                              self.invalid_put34_OddISBN13_2,
                              self.invalid_put35_OddISBN10_2,
                              self.invalid_put36_OddISBN13_3,
                              self.invalid_put37_OddISBN10_3,
                              self.invalid_put38_OddISBN13_4,
                              self.invalid_put39_OddISBN10_4,
                              self.invalid_put40_OddISBN13_5,
                              self.invalid_put41_OddISBN10_5,
                              self.invalid_put42_OddISBN10_6]

    def test_invalid_update_book(self):
        print("#########-Test Invalid PUT Admin-#########")
        response = []
        log_in()

        self.assertTrue(self.client.login(username='admin', password='admin'))
        uuid_book = self.book.uuid_book

        # get API response
        response_get = self.client.get("http://127.0.0.1:8000/library/books/")
        # print(response_get.data)  # Debug
        # get data from db
        books = Book.objects.all()

        # Temporary treatment to check the rest of the data.
        for i in range(len(response_get.data)):
            response_get.data[i]['last_user'] = None
            del response_get.data[i]['uuid_loan']

        serializer_before = BookSerializer(books, many=True)
        self.assertEqual(response_get.data,  # ['data']
                         serializer_before.data)

        # Put invalid data
        for i in range(len(self.invalid_books)):
            response.append(self.client.put("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                            .format(uuid_book=uuid_book),
                                            data=json.dumps(self.invalid_books[i]),
                                            content_type='application/json'))

            # print(">>", i, response[i].data)  # Debug
            self.assertEqual(response[i].status_code, status.HTTP_409_CONFLICT)

            # get data from db
            books_updated = Book.objects.all()
            serializer_invalid = BookSerializer(books_updated, many=True)
            # compare changes:
            self.assertEqual(serializer_invalid.data, serializer_before.data)


class DeleteBookTest(APITestCase):
    global json_data

    def setUp(self):
        self.user = User.objects.create_user(username="user1",
                                             email="",
                                             password="user1")
        self.user.save()

        self.book = Book()
        self.book.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                            editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                            isbn="978-3-16-148410-0", user=self.user)

        self.book_delete = Book()
        self.book_delete.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                                   editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                                   isbn="978-3-16-148410-0", user=self.user)

    def test_delete_book(self):
        print("#########-Test DELETE Book Logged-#########")
        log_in()
        self.assertTrue(self.client.login(username='admin', password='admin'))

        uuid_book = self.book_delete.uuid_book

        # get data from db
        history = History.objects.all()
        serializer_before = HistorySerializer(history, many=True)

        response = self.client.delete("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                      .format(uuid_book=uuid_book),
                                      content_type='application/json')

        # print("<<Del>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get data from db
        history = History.objects.all()
        serializer_after = HistorySerializer(history, many=True)

        self.assertNotEqual(serializer_before, serializer_after.data)

        response = self.client.get("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                   .format(uuid_book=uuid_book),
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

        response = self.client.get("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                   .format(uuid_book=uuid_book),
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_book_NoStaff(self):
        print("#########-Test DELETE Book NoStaff-#########")
        self.assertTrue(self.client.login(username='user1', password='user1'))

        uuid_book = self.book_delete.uuid_book

        response = self.client.delete("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                      .format(uuid_book=uuid_book),
                                      content_type='application/json')

        # print("<<Del>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_UnLogged(self):
        print("#########-Test DELETE Book UnLogged-#########")
        uuid_book = self.book_delete.uuid_book

        response = self.client.delete("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                      .format(uuid_book=uuid_book),
                                      content_type='application/json')

        # print("<<Del>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_rented(self):
        print("#########-Test DELETE Book Rented-#########")
        log_in()
        uuid_book = self.book_delete.uuid_book
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # Rent book
        response_rent = self.client.post("http://127.0.0.1:8000/library/history/",
                                         data=json.dumps({
                                             'uuid_book': str(self.book_delete.uuid_book),
                                             'pk': self.user.pk
                                         }),
                                         content_type='application/json')

        # print(">>", response_rent.data)     # Debug

        uuid_history = response_rent.data['uuid_loan']

        # print(">>DBR>>", uuid_history)  # Debug

        self.assertEqual(response_rent.status_code,
                         status.HTTP_201_CREATED)

        response = self.client.delete("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                      .format(uuid_book=uuid_book),
                                      content_type='application/json')

        # print(">>", response.data)  # Debug

        response = self.client.get("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                   .format(uuid_book=uuid_book),
                                   content_type='application/json')

        # print(">>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

        response = self.client.get("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                   .format(uuid_book=uuid_book),
                                   content_type='application/json')

        # print(">>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_restore_book(self):
        print("#########-Test RESTORE Book-#########")
        log_in()
        uuid_book = self.book_delete.uuid_book
        self.assertTrue(self.client.login(username='admin', password='admin'))

        response = self.client.delete("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                      .format(uuid_book=uuid_book),
                                      content_type='application/json')

        # print(">>", response.data)  # Debug

        response = self.client.put("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                   .format(uuid_book=uuid_book),
                                   data=json.dumps({
                                       'title': "For delete",
                                       'uuid_book': "something",
                                       'description': "For delete.",
                                       'author': "Leandrous",
                                       'editorial': "Sewania",
                                       'language': "English",
                                       'isbn': "0 19 852663 6",
                                       'deleted_book': False
                                   }),
                                   content_type='application/json')

        # print(">>", response.data)  # Debug

        self.client.logout()

        response = self.client.get("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                   .format(uuid_book=uuid_book),
                                   content_type='application/json')

        # print(">>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_book_not_found(self):
        print("#########-Test DELETE Book Not Found-#########")
        log_in()
        self.assertTrue(self.client.login(username='admin', password='admin'))

        response = self.client.delete("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                      .format(uuid_book="bb169a8d-c609-4ecc-b447-c4fd0bf5a644"),
                                      content_type='application/json')

        # print("<<Del>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ValidRentReserveRecoverDeleteBookTest(APITestCase):
    global json_data

    def setUp(self):
        log_in()
        self.user = User.objects.create_user(username="user1",
                                             email="",
                                             password="user1")
        self.user.save()

        self.user2 = User.objects.create_user(username="user2",
                                              email="",
                                              password="user2")
        self.user2.save()

        self.book = Book()
        self.book.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                            editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                            isbn="978-3-16-148410-0", user=self.user)

        self.book_delete = Book()
        self.book_delete.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                                   editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                                   isbn="978-3-16-148410-0", user=self.user)

    def test_rent_book(self):
        print("#########-Test POST RentBook Logged-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/")
        # get data from db
        history = History.objects.all()
        serializer_before = HistorySerializer(history, many=True)

        # print("->>>>>>", response.data)  # Debug  # ['data']

        # Rent
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user.pk
                                    }),
                                    content_type='application/json')

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

        # get data from db
        history = History.objects.all()
        serializer_after = HistorySerializer(history, many=True)

        # print("->>>>>>", response.data)  # Debug  # ['data']

        self.assertNotEqual(serializer_before, serializer_after.data)

    def test_rent_book_noStaff(self):
        print("#########-Test POST RentBook noStaff-#########")
        self.assertTrue(self.client.login(username='user1', password='user1'))
        self.assertFalse(self.user.is_staff)

        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user.pk
                                    }),
                                    content_type='application/json')

        # print("<<Rns>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reserve_book(self):
        print("#########-Test POST ReserveBook Logged-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/")
        # get data from db
        history = History.objects.all()
        serializer_before = HistorySerializer(history, many=True)

        # print("->>>>>>", response.data)  # Debug  # ['data']

        # Rent
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user.pk,
                                        'reserved_book': False
                                    }),
                                    content_type='application/json')

        # print("<<Reserve>>", response.data)     # Debug

        # Reserve
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user2.pk,
                                        'reserved_book': True
                                    }),
                                    content_type='application/json')

        # print("<<Reserve>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Can't Reserve
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user2.pk,
                                        'reserved_book': True
                                    }),
                                    content_type='application/json')

        # print("<<Reserve2>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # get data from db
        history = History.objects.all()
        serializer_after = HistorySerializer(history, many=True)

        self.assertNotEqual(serializer_before, serializer_after.data)

    def test_rent_afterReserve_book(self):
        print("#########-Test POST RentBook After Reserve-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # Rent by other
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user.pk,
                                        'reserved_book': False
                                    }),
                                    content_type='application/json')

        uuid_loan = response.data['uuid_loan']

        # print("<<RentR>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Reserve
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user2.pk,
                                        'reserved_book': True
                                    }),
                                    content_type='application/json')

        # print("<<ReserveR>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Recover
        response = self.client.put("http://127.0.0.1:8000/library/history/{uuid_loan}/"
                                   .format(uuid_loan=str(uuid_loan)),
                                   data=json.dumps({
                                       'uuid_book': str(self.book.uuid_book),
                                       'pk': self.user.pk,
                                       'renew_loan': False
                                   }),
                                   content_type='application/json')

        # print("<<RecoverR>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Rent
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user2.pk,
                                        'reserved_book': False
                                    }),
                                    content_type='application/json')

        # print("<<RentR2>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cancel_reserve_book(self):
        print("#########-Test Put Cancel Reserve Book-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # Reserve
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user2.pk,
                                        'reserved_book': True
                                    }),
                                    content_type='application/json')

        uuid_loan = response.data['uuid_loan']

        # print("<<Reserve>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Cancel reserve
        response = self.client.put("http://127.0.0.1:8000/library/history/{uuid_loan}/"
                                   .format(uuid_loan=str(uuid_loan)),
                                   data=json.dumps({
                                       'uuid_book': str(self.book.uuid_book),
                                       'pk': self.user2.pk,
                                       'renew_loan': False
                                   }),
                                   content_type='application/json')

        # print("<<Cancel R>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recover_book(self):
        print("#########-Test PUT RecoverBook Logged-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # Rent Book
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user.pk
                                    }),
                                    content_type='application/json')

        # print(">>Reco>", response.data)     # Debug

        uuid_loan = response.data['uuid_loan']

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

        # get data from db
        history = History.objects.all()
        serializer_before = HistorySerializer(history, many=True)

        self.assertNotEqual(response.data,  # ['data']
                            serializer_before.data)

        # Recover Book
        response = self.client.put("http://127.0.0.1:8000/library/history/{uuid_loan}/"
                                   .format(uuid_loan=str(uuid_loan)),
                                   data=json.dumps({
                                       'uuid_book': str(self.book.uuid_book),
                                       'pk': self.user.pk,
                                       'renew_loan': False
                                   }),
                                   content_type='application/json')

        # print("<<Recover>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get data from db
        history = History.objects.all()
        serializer_after = HistorySerializer(history, many=True)

        # print("->>>>>>", response.data)  # Debug  # ['data']

        self.assertNotEqual(serializer_before, serializer_after.data)

    def test_recover_book_noStaff(self):
        print("#########-Test PUT RecoverBook NoStaff-#########")
        self.assertTrue(self.client.login(username='user1', password='user1'))
        self.assertFalse(self.user.is_staff)

        # Rent Book
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user.pk
                                    }),
                                    content_type='application/json')

        # print(">>>>>>", response.data)  # Debug

        uuid_loan = response.data['uuid_loan']

        # Recover
        response = self.client.put("http://127.0.0.1:8000/library/history/{uuid_loan}/"
                                   .format(uuid_loan=str(uuid_loan)),
                                   data=json.dumps({
                                       'uuid_book': str(self.book.uuid_book),
                                       'pk': self.user.pk,
                                       'renew_loan': False
                                   }),
                                   content_type='application/json')

        # print(">>>>>>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_renew_history(self):
        print("#########-Test PUT RecoverBook Logged-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # Rent Book
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user.pk
                                    }),
                                    content_type='application/json')

        # print(">>Reco>", response.data)     # Debug

        uuid_loan = response.data['uuid_loan']
        date_before = response.data['date_finished_loan']

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)

        # get data from db
        history = History.objects.all()
        serializer_before = HistorySerializer(history, many=True)

        self.assertNotEqual(response.data,  # ['data']
                            serializer_before.data)

        # Renew Book
        response = self.client.put("http://127.0.0.1:8000/library/history/{uuid_loan}/"
                                   .format(uuid_loan=str(uuid_loan)),
                                   data=json.dumps({
                                       'uuid_book': str(self.book.uuid_book),
                                       'pk': self.user.pk,
                                       'renew_loan': True
                                   }),
                                   content_type='application/json')

        date_after = response.data['date_finished_loan']

        # print("<<Recover>>", response.data)     # Debug

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(date_before, date_after)

        # get data from db
        history = History.objects.all()
        serializer_after = HistorySerializer(history, many=True)

        self.assertNotEqual(serializer_before, serializer_after.data)


class InvalidRentRecoverDeleteBookTest(APITestCase):
    global json_data

    def setUp(self):
        # Users
        self.user = User.objects.create_user(username="user1",
                                             email="",
                                             password="user1")
        self.user.save()

        self.user2 = User.objects.create_user(username="user2",
                                              email="",
                                              password="user2")
        self.user2.save()

        self.user3 = User.objects.create_user(username="user4",
                                              email="",
                                              password="user4")

        # Books
        self.book = Book()
        self.book.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                            editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                            isbn="978-3-16-148410-0", user=self.user)

        self.book.save()

        self.bookNoAvailable = Book()
        self.bookNoAvailable.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                                       editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                                       isbn="978-3-16-148410-0", user=self.user)
        self.bookNoAvailable.save()

        self.book_double_recover = Book()
        self.book_double_recover.edit_book(title=json_data[0]['Title'], description="",
                                           author=json_data[0]['Authors'][0],
                                           editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                                           isbn="978-3-16-148410-0", user=self.user)
        self.book_double_recover.save()

        self.book_rented = Book()
        self.book_rented.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                                   editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                                   isbn="978-3-16-148410-0", user=self.user)
        self.book_rented.save()

        self.bookMT3_1 = Book()
        self.bookMT3_1.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                                 editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                                 isbn="978-3-16-148410-0", user=self.user)
        self.bookMT3_2 = Book()
        self.bookMT3_2.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                                 editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                                 isbn="978-3-16-148410-0", user=self.user)
        self.bookMT3_3 = Book()
        self.bookMT3_3.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                                 editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                                 isbn="978-3-16-148410-0", user=self.user)

        self.userMT3 = User.objects.create_user(username="userMT3",
                                                email="",
                                                password="userMT3")
        self.userMT3.save()

        # Others

        self.booksMT3 = [self.bookMT3_1, self.bookMT3_2, self.bookMT3_3]

        # Rent books
        log_in()
        self.client.login(username='admin', password='admin')

        self.client.post("http://127.0.0.1:8000/library/history/",
                         data=json.dumps({
                             'uuid_book': str(self.bookNoAvailable.uuid_book),
                             'pk': self.user2.pk
                         }),
                         content_type='application/json')

        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book_double_recover.uuid_book),
                                        'pk': self.user3.pk
                                    }),
                                    content_type='application/json')

        self.uuid_loanDoubleRecover = response.data['uuid_loan']

        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book_rented.uuid_book),
                                        'pk': self.user2.pk
                                    }),
                                    content_type='application/json')

        self.uuid_loanInvalidRecov = response.data['uuid_loan']

        self.client.logout()

        # Invalid Rents
        self.invalid_rent0_BadPK1 = {
            'pk': None,
            'uuid_book': str(self.book.uuid_book)
        }
        self.invalid_rent1_BadPK2 = {
            'pk': 0,
            'uuid_book': str(self.book.uuid_book)
        }
        self.invalid_rent2_BadPK3 = {
            'pk': 'I dont exist',
            'uuid_book': str(self.book.uuid_book)
        }
        self.invalid_rent3_BadUUID_BOOK1 = {
            'pk': self.user.pk,
            'uuid_book': '1232456414e356754'
        }
        self.invalid_rent4_BadUUID_BOOK2 = {
            'pk': self.user.pk,
            'uuid_book': 22343545
        }
        self.invalid_rent5_BadUUID_BOOK3 = {
            'pk': self.user.pk,
            'uuid_book': None
        }
        self.invalid_rent6_MoreThan3 = {
            'pk': self.userMT3.pk,
            'uuid_book': str(self.book.uuid_book)
        }
        self.invalid_rent7_NoAvailableBook = {
            'pk': self.user.pk,
            'uuid_book': str(self.bookNoAvailable.uuid_book)
        }

        self.invalid_rents = [self.invalid_rent0_BadPK1,
                              self.invalid_rent1_BadPK2,
                              self.invalid_rent2_BadPK3,
                              self.invalid_rent3_BadUUID_BOOK1,
                              self.invalid_rent4_BadUUID_BOOK2,
                              self.invalid_rent5_BadUUID_BOOK3,
                              self.invalid_rent6_MoreThan3,
                              self.invalid_rent7_NoAvailableBook]

        # Invalid recovers
        self.invalid_recov0_OddPk = {
            'pk': "hello",
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': False
        }
        self.invalid_recov1_emptyPk = {
            'pk': "",
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': False
        }
        self.invalid_recov2_noPk = {
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': False
        }
        self.invalid_recov3_NonePk = {
            'pk': None,
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': False
        }
        self.invalid_recov4_number0Pk = {
            'pk': 0,
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': False
        }
        self.invalid_recov5_OddUUID = {
            'pk': self.user2.pk,
            'uuid_book': "odd_uuid gegege",
            'renew_loan': False
        }
        self.invalid_recov6_emptyUUID = {
            'pk': self.user2.pk,
            'uuid_book': "",
            'renew_loan': False
        }
        self.invalid_recov7_noUUID = {
            'pk': self.user2.pk,
            'renew_loan': False
        }
        self.invalid_recov8_NoneUUID = {
            'pk': self.user2.pk,
            'uuid_book': None,
            'renew_loan': False
        }
        self.invalid_recov9_OtherUser = {
            'pk': self.user.pk,
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': False
        }
        self.invalid_recov10_OtherBook = {
            'pk': self.user2.pk,
            'uuid_book': str(self.book.uuid_book),
            'renew_loan': False
        }
        self.invalid_recov11_OddRenew1 = {
            'pk': self.user2.pk,
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': "fal"
        }
        self.invalid_recov12_OddRenew2 = {
            'pk': self.user2.pk,
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': "tru"
        }
        self.invalid_recov13_NoneRenew = {
            'pk': self.user2.pk,
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': None
        }
        self.invalid_recov14_NumberRenew = {
            'pk': self.user2.pk,
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': 0
        }

        self.invalid_recovs = [self.invalid_recov0_OddPk,
                               self.invalid_recov1_emptyPk,
                               self.invalid_recov2_noPk,
                               self.invalid_recov3_NonePk,
                               self.invalid_recov4_number0Pk,
                               self.invalid_recov5_OddUUID,
                               self.invalid_recov6_emptyUUID,
                               self.invalid_recov7_noUUID,
                               self.invalid_recov8_NoneUUID,
                               self.invalid_recov9_OtherUser,
                               self.invalid_recov10_OtherBook,
                               self.invalid_recov11_OddRenew1,
                               self.invalid_recov12_OddRenew2,
                               self.invalid_recov13_NoneRenew,
                               self.invalid_recov14_NumberRenew]

        # Invalid renews
        self.invalid_renew0_OddPk = {
            'pk': "hello",
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': True
        }
        self.invalid_renew1_emptyPk = {
            'pk': "",
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': True
        }
        self.invalid_renew2_noPk = {
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': True
        }
        self.invalid_renew3_NonePk = {
            'pk': None,
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': True
        }
        self.invalid_renew4_number0Pk = {
            'pk': 0,
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': True
        }
        self.invalid_renew5_OddUUID = {
            'pk': self.user2.pk,
            'uuid_book': "odd_uuid gegege",
            'renew_loan': True
        }
        self.invalid_renew6_emptyUUID = {
            'pk': self.user2.pk,
            'uuid_book': "",
            'renew_loan': True
        }
        self.invalid_renew7_noUUID = {
            'pk': self.user2.pk,
            'renew_loan': True
        }
        self.invalid_renew8_NoneUUID = {
            'pk': self.user2.pk,
            'uuid_book': None,
            'renew_loan': True
        }
        self.invalid_renew9_OtherUser = {
            'pk': self.user.pk,
            'uuid_book': str(self.book_rented.uuid_book),
            'renew_loan': True
        }
        self.invalid_renew10_OtherBook = {
            'pk': self.user2.pk,
            'uuid_book': str(self.book.uuid_book),
            'renew_loan': True
        }

        self.invalid_renews = [self.invalid_renew0_OddPk, self.invalid_renew1_emptyPk,
                               self.invalid_renew2_noPk, self.invalid_renew3_NonePk,
                               self.invalid_renew4_number0Pk, self.invalid_renew5_OddUUID,
                               self.invalid_renew6_emptyUUID, self.invalid_renew7_noUUID,
                               self.invalid_renew8_NoneUUID, self.invalid_renew9_OtherUser,
                               self.invalid_renew10_OtherBook]

    def test_rent_book_unLogged(self):
        print("#########-Test POST RentBook UnLogged-#########")
        response = self.client.post("http://127.0.0.1:8000/library/history/",
                                    data=json.dumps({
                                        'uuid_book': str(self.book.uuid_book),
                                        'pk': self.user.pk
                                    }),
                                    content_type='application/json')

        # print(">>", response.data)

        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_invalid_rent_book(self):
        print("#########-Test POST Invalid RentBook-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))
        self.assertFalse(self.user.is_staff)

        # Data for tests No More Than 3 books.
        for i in range(len(self.booksMT3)):
            self.client.post("http://127.0.0.1:8000/library/history/",
                             data=json.dumps({
                                 'uuid_book': str(self.booksMT3[i].uuid_book),
                                 'pk': self.userMT3.pk
                             }),
                             content_type='application/json')

        for i in range(len(self.invalid_rents)):
            response = self.client.post("http://127.0.0.1:8000/library/history/",
                                        data=json.dumps(self.invalid_rents[i]),
                                        content_type='application/json')

            # print(">>", i, response.data)  # Debug

            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_recover_book_unLogged(self):
        print("#########-Test POST RecoverBook UnLogged-#########")

        response = self.client.put("http://127.0.0.1:8000/library/history/",
                                   data=json.dumps({
                                       'uuid_book': str(self.book.uuid_book),
                                       'pk': self.user.pk,
                                       'renew_loan': False
                                   }),
                                   content_type='application/json')

        # print(">>>>>>", response.data)  # Debug

        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_invalid_recover_book(self):
        print("#########-Test PUT RecoverBook-#########")  # Incomplete
        self.assertTrue(self.client.login(username='admin', password='admin'))

        for i in range(len(self.invalid_recovs)):
            response = self.client.put("http://127.0.0.1:8000/library/history/{uuid_loan}/"
                                       .format(uuid_loan=str(self.uuid_loanInvalidRecov)),
                                       data=json.dumps(self.invalid_recovs[i]),
                                       content_type='application/json')

            # print(">>", i, ">>", response.data)  # Debug

            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        response = self.client.put("http://127.0.0.1:8000/library/history/{uuid_loan}/"
                                   .format(uuid_loan='fe58b1f7-08a4-4118-9a63-4d88d696a310'),
                                   data=json.dumps({
                                       'uuid_book': str(self.book.uuid_book),
                                       'pk': self.user.pk,
                                       'renew_loan': False
                                   }),
                                   content_type='application/json')

        # print(">>id_loanRecov>>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_invalid_renew_history(self):
        print("#########-Test PUT RecoverBook-#########")  # Incomplete
        self.assertTrue(self.client.login(username='admin', password='admin'))

        for i in range(len(self.invalid_renews)):
            response = self.client.put("http://127.0.0.1:8000/library/history/{uuid_loan}/"
                                       .format(uuid_loan=str(self.uuid_loanInvalidRecov)),
                                       data=json.dumps(self.invalid_renews[i]),
                                       content_type='application/json')

            # print(">>", i, ">>", response.data)  # Debug

            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_invalid_double_recover_or_renew_book(self):
        print("#########-Test PUT RecoverBook Double-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        response = self.client.put("http://127.0.0.1:8000/library/history/{uuid_loan}/"
                                   .format(uuid_loan=str(self.uuid_loanDoubleRecover)),
                                   data=json.dumps({
                                       'uuid_book': str(self.book_double_recover.uuid_book),
                                       'pk': self.user3.pk,
                                       'renew_loan': False
                                   }),
                                   content_type='application/json')

        # print(">>Rec>>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put("http://127.0.0.1:8000/library/history/{uuid_loan}/"
                                   .format(uuid_loan=str(self.uuid_loanDoubleRecover)),
                                   data=json.dumps({
                                       'uuid_book': str(self.book_double_recover.uuid_book),
                                       'pk': self.user3.pk,
                                       'renew_loan': False
                                   }),
                                   content_type='application/json')

        # print(">>i.Rec>>", response.data)  # Debug

        self.assertEqual(response.status_code,
                         status.HTTP_409_CONFLICT)

        response = self.client.put("http://127.0.0.1:8000/library/history/{uuid_loan}/"
                                   .format(uuid_loan=str(self.uuid_loanDoubleRecover)),
                                   data=json.dumps({
                                       'uuid_book': str(self.book_double_recover.uuid_book),
                                       'pk': self.user3.pk,
                                       'renew_loan': True
                                   }),
                                   content_type='application/json')

        # print(">>i.Rec>>", response.data)  # Debug

        self.assertEqual(response.status_code,
                         status.HTTP_409_CONFLICT)

    def test_delete_book_unLogged(self):
        print("#########-Test DELETE Book UnLogged-#########")

        uuid_book = self.book.uuid_book

        response = self.client.delete("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                      .format(uuid_book=uuid_book),
                                      content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_noStaff(self):
        print("#########-Test DELETE Book NoStaff-#########")
        uuid_book = self.book.uuid_book
        self.assertTrue(self.client.login(username='user1', password='user1'))

        response = self.client.delete("http://127.0.0.1:8000/library/books/{uuid_book}/"
                                      .format(uuid_book=uuid_book),
                                      content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetBookHistoryTest(APITestCase):
    global json_data

    def setUp(self):
        self.user = User.objects.create_user(username="user1",
                                             email="",
                                             password="user1")
        self.user.save()
        self.book = Book()
        self.book.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                            editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                            isbn="978-3-16-148410-0", user=self.user)

        self.user2 = User.objects.create_user(username="user2",
                                              email="",
                                              password="user2")
        self.user2.save()

        self.history = History()

        log_in()

        self.client.login(username='admin', password='admin')
        self.client.post("http://127.0.0.1:8000/library/history/",
                         data=json.dumps({
                             'uuid_book': str(self.book.uuid_book),
                             'pk': self.user.pk
                         }),
                         content_type='application/json')

        self.client.logout()

    def test_get_books_history(self):
        print("#########-Test GET History Logged-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/")
        # get data from db
        history = History.objects.all()
        serializer = HistorySerializer(history, many=True)

        # print("->>>>>>", response.data)  # Debug  # ['data']

        # Temporary treatment to check the rest of the data.
        for i in range(len(response.data)):
            response.data[i]['book']['last_user'] = None

        self.assertEqual(response.data,  # ['data']
                         serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_books_history_UnLogged(self):
        print("#########-Test GET History UnLogged-#########")
        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/")
        # get data from db
        history = History.objects.all()
        serializer = HistorySerializer(history, many=True)

        # print("->>>>>>", response.data)  # Debug  # ['data']

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_books_history_NoStaff(self):
        print("#########-Test GET History noStaff-#########")
        self.assertTrue(self.client.login(username='user1', password='user1'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/")
        # get data from db
        history = History.objects.all()
        serializer = HistorySerializer(history, many=True)

        # print("->>>>>>", response.data)  # Debug  # ['data']

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_history(self):
        print("#########-Test GET User History-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/user/{}/".format(self.user.pk))
        # get data from db
        history = History.objects.filter(user=self.user)
        serializer = HistorySerializer(history, many=True)

        # print("->>>>>>", response.data)  # Debug  # ['data']

        # Temporary treatment to check the rest of the data.
        for i in range(len(response.data)):
            response.data[0]['book']['last_user'] = None

        self.assertEqual(response.data,  # ['data']
                         serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_history_UnLogged(self):
        print("#########-Test GET User History UnLogged-#########")

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/user/{}/".format(self.user.pk))

        # print("->>>>>>", response.data)  # Debug  # ['data']

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_history_NoStaff(self):
        print("#########-Test GET User History NoStaff-#########")
        self.assertTrue(self.client.login(username='user2', password='user2'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/user/{}/".format(self.user.pk))

        # print("->>>>>>", response.data)  # Debug  # ['data']

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_history_owner(self):
        print("#########-Test GET User History Owner-#########")
        self.assertTrue(self.client.login(username='user1', password='user1'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/user/{}/".format(self.user.pk))
        # get data from db
        history = History.objects.filter(user=self.user)
        serializer = HistorySerializer(history, many=True)

        # print("->>>>>>", response.data)  # Debug  # ['data']

        # Temporary treatment to check the rest of the data.
        for i in range(len(response.data)):
            response.data[0]['book']['last_user'] = None

        self.assertEqual(response.data,  # ['data']
                         serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_book_history(self):
        print("#########-Test GET Book History-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/book/{}/".format(self.book.uuid_book))
        # get data from db
        history = History.objects.filter(book=self.book)
        serializer = HistorySerializer(history, many=True)

        # print("->>>>>>", response.data)  # Debug  # ['data']

        # Temporary treatment to check the rest of the data.
        for i in range(len(response.data)):
            response.data[0]['book']['last_user'] = None

        self.assertEqual(response.data,  # ['data']
                         serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_book_history_UnLogged(self):
        print("#########-Test GET Book History UnLogged-#########")

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/book/{}/".format(self.book.uuid_book))

        # print("->>>>>>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_book_history_NoStaff(self):
        print("#########-Test GET Book History NoStaff-#########")
        self.assertTrue(self.client.login(username='user1', password='user1'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/book/{}/".format(self.book.uuid_book))

        # print("->>>>>>", response.data)  # Debug  # ['data']

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_history_404(self):
        print("#########-Test GET User History-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/user/2133/")

        # print("->>>>>>", response)  # Debug
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_book_history_404(self):
        print("#########-Test GET Book History NotFound-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/library/history/book/a378a1e7-25f8-4d39-b457-374770620d11/")

        # print("->>>>>>", response)  # Debug
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteBookHistoryTest(APITestCase):
    global json_data

    def setUp(self):
        self.user = User.objects.create_user(username="user1",
                                             email="",
                                             password="user1")
        self.user.save()
        self.book = Book()
        self.book.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                            editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                            isbn="978-3-16-148410-0", user=self.user)

        self.history = History()

        log_in()

        self.client.login(username='admin', password='admin')
        self.client.post("http://127.0.0.1:8000/library/history/",
                         data=json.dumps({
                             'uuid_book': str(self.book.uuid_book),
                             'pk': self.user.pk
                         }),
                         content_type='application/json')

        self.client.logout()

    def test_delete_history(self):
        print("#########-Test Delete History-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get data from db
        history = History.objects.all()
        serializer_before = HistorySerializer(history, many=True)

        # get API response
        response = self.client.delete("http://127.0.0.1:8000/library/history/{}/"
                                      .format(self.history.uuid_loan))

        # get data from db
        history = History.objects.all()
        serializer_after = HistorySerializer(history, many=True)

        # print("->>>>>>", response.data)  # Debug  # ['data']

        self.assertEqual(serializer_before.data, serializer_after.data)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_history_UnLogged(self):
        print("#########-Test Delete History UnLogged-#########")

        # get API response
        response = self.client.delete("http://127.0.0.1:8000/library/history/{}/"
                                      .format(self.history.uuid_loan))

        # print("->>>>>>", response.data)  # Debug  # ['data']
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_delete_history_NoStaff(self):
        print("#########-Test Delete History NoStaff-#########")
        self.assertTrue(self.client.login(username='user1', password='user1'))

        # get API response
        response = self.client.delete("http://127.0.0.1:8000/library/history/{}/"
                                      .format(self.history.uuid_loan))

        # print("->>>>>>", response.data)  # Debug  # ['data']
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)


class ISBNLibGoogleApiTest(APITestCase):
    def setUp(self):
        log_in()

        User.objects.create_user(username="user1", email="user1@api.com", password="user1")

        # Valid isbns
        self.valid_isbn0_13 = {
            'isbn': "9783161484100"
        }
        self.valid_isbn1_13 = {
            'isbn': "978-0316029186"
        }
        self.valid_isbn2_13 = {
            'isbn': "978 3 16 148410 0"
        }
        self.valid_isbn3_10 = {
            'isbn': "842261586X"
        }
        self.valid_isbn4_10 = {
            'isbn': "0-19-852663-6"
        }
        self.valid_isbn5_10 = {
            'isbn': "0 19 852663 6"
        }

        # Invalid isbns
        self.invalid_isbn0_13_odd1 = {
            'isbn': "978316148410000000"
        }
        self.invalid_isbn1_13_odd2 = {
            'isbn': "9783161484100Avalon"
        }
        self.invalid_isbn2_13_odd3 = {
            'isbn': "978316148410X"
        }
        self.invalid_isbn3_13_odd4 = {
            'isbn': "9783161484100-Z"
        }
        self.invalid_isbn4_10_odd1 = {
            'isbn': "842261586X0000"
        }
        self.invalid_isbn5_10_odd2 = {
            'isbn': "0-19-852663-6Avalon"
        }
        self.invalid_isbn6_10_odd3 = {
            'isbn': "842261586X-Z"
        }
        self.invalid_isbn7_10_odd4 = {
            'isbn': "0 19 852663 6 _ "
        }
        self.invalid_isbn8_13_empty = {
            'isbn': ""
        }
        self.invalid_isbn9_13_none = {
            'isbn': None
        }
        self.invalid_isbn10_13_noIsbn = {
            'aux': "Nothing"
        }
        self.invalid_isbn11_13_list = {
            'isbn': list()
        }

        self.valid_isbns = [self.valid_isbn0_13, self.valid_isbn1_13, self.valid_isbn2_13,
                            self.valid_isbn3_10, self.valid_isbn4_10, self.valid_isbn5_10]

        self.invalid_isbns = [self.invalid_isbn0_13_odd1,
                              self.invalid_isbn1_13_odd2,
                              self.invalid_isbn2_13_odd3,
                              self.invalid_isbn3_13_odd4,
                              self.invalid_isbn4_10_odd1,
                              self.invalid_isbn5_10_odd2,
                              self.invalid_isbn6_10_odd3,
                              self.invalid_isbn7_10_odd4,
                              self.invalid_isbn8_13_empty,
                              self.invalid_isbn9_13_none,
                              self.invalid_isbn10_13_noIsbn,
                              self.invalid_isbn11_13_list]

    def test_find_ISBNLib_Api(self):  # Mocked to avoid the error "Too many requests"
        print("#########-Test Find Book in Google Api-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        for i in range(len(self.valid_isbns)):
            mock_data = mock_book_data(self, i)

            with patch('Library.views.ApiResults') as mock_requests:
                mock_requests().data_book = mock_data

                response = self.client.post("http://127.0.0.1:8000/library/find/",
                                            data=json.dumps(self.valid_isbns[i]),
                                            content_type='application/json')

                # print(">>G.Api-V>>", response.data)  # Debug

                self.assertTrue(response.status_code, status.HTTP_200_OK)

                self.assertEqual(response.data, mock_data)

    def test_find_ISBNLib_Api_invalid(self):
        print("#########-Test Find Book in Google Api Invalid ISBN-#########")
        self.assertTrue(self.client.login(username='admin', password='admin'))

        for i in range(len(self.valid_isbns)):
            response = self.client.post("http://127.0.0.1:8000/library/find/",
                                        data=json.dumps(self.invalid_isbns[i]),
                                        content_type='application/json')

            # print(">>G.Api-IV>>", response.data)  # Debug

            self.assertTrue(response.status_code, status.HTTP_409_CONFLICT)

    def test_find_ISBNLib_Api_NoStaff(self):
        print("#########-Test Find Book in Google Api NoStaff-#########")
        self.assertTrue(self.client.login(username='user1', password='user1'))

        for i in range(len(self.valid_isbns)):
            response = self.client.post("http://127.0.0.1:8000/library/find/",
                                        data=json.dumps({
                                            "isbn": '9780316029186'
                                        }),
                                        content_type='application/json')

            # print(">>G.Api-V>>", response.data)  # Debug

            self.assertTrue(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_find_ISBNLib_Api_UnLogged(self):
        print("#########-Test Find Book in Google Api UnLogged-#########")
        self.assertTrue(self.client.login(username='user1', password='user1'))

        for i in range(len(self.valid_isbns)):
            response = self.client.post("http://127.0.0.1:8000/library/find/",
                                        data=json.dumps({
                                            "isbn": '9780316029186'
                                        }),
                                        content_type='application/json')

            # print(">>G.Api-V>>", response.data)  # Debug

            self.assertTrue(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OtherLibraryTests(APITestCase):
    global json_data

    def setUp(self):
        self.user = User.objects.create_user(username="user1",
                                             email="",
                                             password="user1")
        self.user.save()
        self.book = Book()
        self.book.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'][0],
                            editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                            isbn="978-3-16-148410-0", user=self.user)
        self.book.save()

    def test_edit_book(self):  # Before called create_book.
        print("#########-Test Create Again Book-#########")
        log_in()
        book_uuid_1 = self.book.uuid_book
        updated_time_1 = self.book.updated_time
        updated_user_1 = self.book.updated_user

        self.book.edit_book(title=json_data[0]['Title'], description="", author=json_data[0]['Authors'],
                            editorial=json_data[0]['Publisher'], language=json_data[0]['Language'],
                            isbn="978-3-16-148410-0", user=User.objects.get(username="admin"))
        self.book.save()

        book_uuid_2 = self.book.uuid_book
        updated_time_2 = self.book.updated_time
        updated_user_2 = self.book.updated_user

        # print(">>CB>>", book_uuid_1, "-", book_uuid_2)  # Debug

        self.assertEqual(book_uuid_1, book_uuid_2)  # When method was called create_book, this was assertNotEqual.
        self.assertNotEqual(updated_time_1, updated_time_2)
        self.assertNotEqual(updated_user_1, updated_user_2)

    def test_patch_book(self):
        log_in()
        self.assertTrue(self.client.login(username='admin', password='admin'))

        response = self.client.patch("http://127.0.0.1:8000/library/books/",
                                     data=json.dumps({
                                         'hello': "Hi hi"
                                     }),
                                     content_type='application/json')

        # print(">>Rare>>", response)     # Debug
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
