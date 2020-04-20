import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from Library.models import Book, History
from Login.serializers import UserSerializer


# The tests do not use paging.

def log_in():
    admin = User.objects.create_superuser(username="admin",
                                          email="",
                                          password="admin")
    admin.save()


json_data = {
    'ISBN-13': '9783161484100',
    'Title': 'An Essay Commissioned For The Exhibition: "Regarding Henry\'s Show" @ The Brant Foundation Art Study Center, Greenwich, CT, 2009',
    'Authors': [''], 'Publisher': '', 'Year': '2009', 'Language': 'en', 'Desc': None, 'Images': {
        'smallThumbnail': 'http://books.google.com/books/content?id=CtCLAwAAQBAJ&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api',
        'thumbnail': 'http://books.google.com/books/content?id=CtCLAwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'}
}


class GetAllUsersTest(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='TestNormalStaff', email='',
            password='1234', is_staff=True)

        User.objects.create_user(
            username='TestNnoStaff', email='', password='1234')

        User.objects.create_user(
            pk=7, username='TestPkCreate', email='', password='1234')

        User.objects.create_user(
            pk=12, username='TestPkCreateUser', email='', password='1234')

    def test_get_all_users(self):
        print("#########-Test GET users-#########")
        # log_in User
        log_in()
        self.assertTrue(self.client.login(username='admin', password='admin'))
        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/")
        # print(response.data)  # Debug
        # get data from db
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        # print(">>", response.data)

        # It compares the data of the response with those of the database.
        self.assertEqual(response.data,  # ['data']
                         serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users_NoStaff(self):
        print("#########-Test GET users UnLogged-#########")
        self.assertTrue(self.client.login(username='TestNnoStaff', password='1234'))
        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_users_unLogged(self):
        print("#########-Test GET users UnLogged-#########")
        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetUserTest(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='TestUser1', email='', password='1234')
        User.objects.create_user(
            username='TestUser2', email='', password='1234')

    def test_get_user_valid(self):
        print("#########-Test GET User exists-#########")
        log_in()
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/2/")
        # print(response.data)  # Debug
        # get data from db
        user = User.objects.get(pk=2)
        serializer = UserSerializer(user)

        # It compares the data of the response with those of the database.
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_invalid(self):
        print("#########-Test GET User no exists-#########")
        log_in()
        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/30/")
        # print(response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_owner(self):
        print("#########-Test GET User Owner-#########")
        self.assertTrue(
            self.client.login(username='TestUser2', password='1234'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/2/")
        # print(response.data)  # Debug
        # get data from db
        user = User.objects.get(pk=2)
        serializer = UserSerializer(user)

        # It compares the data of the response with those of the database.
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_NoStaff(self):
        print("#########-Test GET User NoStaff-#########")
        self.assertTrue(
            self.client.login(username='TestUser1', password='1234'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/2/")
        # print(response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_unLogged(self):
        print("#########-Test GET User UnLogged-#########")
        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/1/")
        # print(response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ValidPostUserTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1',
                                             email="",
                                             password='user1')

        # Valid
        self.valid_user0 = {
            'username': 'TestValidNoPk1',
            'password': '1234',
            'repeat_password': '1234',
            'email': 'hello.world@gmail.com',
            'first_name': '',
            'last_name': '',
            'is_staff': True
        }
        self.valid_user1 = {
            'username': 'TestValidNoPk2',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': 'Pepito',
            'last_name': '',
            'is_staff': True
        }
        self.valid_user2_pk = {  # It should not assign the pk introduced.
            'username': 'TestValidPk',
            'pk': 30,
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': '',
            'last_name': 'Grillo',
            'is_staff': True
        }
        self.valid_user3_simple = {
            'username': 'TestValidSimple',
            'password': '1234',
            'repeat_password': '1234'
        }
        self.valid_user4 = {
            'username': 'TestValidStaff1',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': "True"
        }
        self.valid_user5 = {
            'username': 'TestValidStaff2',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': "true"
        }
        self.valid_user6 = {
            'username': 'TestValidStaff3',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': "tRUE"
        }
        self.valid_user7 = {
            'username': 'TestValidStaff4',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': "TRUE"
        }
        self.valid_user8 = {
            'username': 'TestValidStaff5',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': "tRue"
        }

        self.valid_users = [self.valid_user0, self.valid_user1,
                            self.valid_user2_pk, self.valid_user3_simple,
                            self.valid_user4, self.valid_user5,
                            self.valid_user6, self.valid_user7,
                            self.valid_user8]

    def test_create_valid_user(self):
        print("#########-Test POST Valid User-#########")
        response_c = []
        log_in()

        for i in range(len(self.valid_users)):
            self.assertTrue(self.client.login(username='admin', password='admin'))

            response_c.append(self.client.post("http://127.0.0.1:8000/login/users/",
                                               data=json.dumps(self.valid_users[i]),
                                               content_type='application/json'))

            # print(">V>>", i, response_c[i].data)  # Debug
            self.assertEqual(response_c[i].status_code, status.HTTP_201_CREATED)

            user = User.objects.get(username=self.valid_users[i]['username'])

            # get API response
            response_g = self.client.get("http://127.0.0.1:8000/login/users/{pk}/".format(pk=user.pk))
            # print(">Vg>>", i, response_g.data)  # Debug
            # get data from db
            serializer = UserSerializer(user)
            # It compares the data of the response with those of the database.
            self.assertEqual(response_g.data, serializer.data)

    def test_create_user_unLogged(self):
        print("#########-Test POST User When UnLogged-#########")
        response = self.client.post("http://127.0.0.1:8000/login/users/",
                                    data=json.dumps({
                                        'username': 'TestValidNoPk1',
                                        'password': '1234',
                                        'repeat_password': '1234',
                                        'email': 'hello.world@gmail.com',
                                        'first_name': '',
                                        'last_name': '',
                                        'is_staff': True
                                    }),
                                    content_type='application/json')

        # print(">>", response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_noStaff(self):
        print("#########-Test POST Valid noStaff-#########")
        self.assertTrue(self.client.login(username='user1', password='user1'))
        self.assertFalse(self.user.is_staff)

        response = self.client.post("http://127.0.0.1:8000/login/users/",
                                    data=json.dumps({
                                        'username': 'TestValidNoPk1',
                                        'password': '1234',
                                        'repeat_password': '1234',
                                        'email': 'hello.world@gmail.com',
                                        'first_name': '',
                                        'last_name': '',
                                        'is_staff': True
                                    }),
                                    content_type='application/json')

        # print(">>", response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class InvalidPostUserTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1',
                                             email="user1@mail.com",
                                             password='user1')

        # Invalids
        User.objects.create_user(
            username='TestInvalidUsername', email='', password='1234')

        self.invalid_user0_username = {
            'username': 'TestInvalidUsername',
            'password': '12534',
            'repeat_password': '12534'
        }

        self.invalid_user1_emptyUsername = {
            'username': '',
            'password': '1234',
            'repeat_password': '1234'
        }
        self.invalid_user2_noUsername = {
            'password': '1234',
            'repeat_password': '1234'
        }
        self.invalid_user3_emptyPassword = {
            'username': 'TestEmptyPassword',
            'password': '',
            'repeat_password': '1234'
        }
        self.invalid_user4_emptyRepeatPassword = {
            'username': 'TestEmptyPassword',
            'password': '1234',
            'repeat_password': ''
        }
        self.invalid_user5_noPassword = {
            'username': 'TestNoPassword',
            'repeat_password': '1234'
        }
        self.invalid_user6_noRepeatPassword = {
            'username': 'TestNoPassword',
            'password': '1234'
        }
        self.invalid_user7_differentPassword = {
            'username': 'TestNoPassword',
            'password': '1234',
            'repeat_password': '4321'
        }
        self.invalid_user8_email_1 = {
            'username': 'TestBadMail',
            'password': '1234',
            'repeat_password': '1234',
            'email': 'mail.invalid'
        }
        self.invalid_user9_email_2 = {
            'username': 'TestBadMail',
            'password': '1234',
            'repeat_password': '1234',
            'email': 'user1@mail.com'
        }
        self.invalid_user10_NoneEmail = {
            'username': 'TestBadMail',
            'password': '1234',
            'repeat_password': '1234',
            'email': None
        }
        self.invalid_user11_NoneFN = {
            'username': 'TestBadFName',
            'password': '1234',
            'repeat_password': '1234',
            'first_name': None
        }
        self.invalid_user12_NoneLN = {
            'username': 'TestBadLName',
            'password': '1234',
            'repeat_password': '1234',
            'last_name': None
        }
        self.invalid_user13_NumberAvailable = {
            'username': 'TestInvalidAvailable1',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': 0
        }
        self.invalid_user23_ListAvailable = {
            'username': 'TestInvalidAvailable1',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': [0, "false"]
        }
        self.invalid_user14_NumberEmail = {
            'username': 'TestInvalidEmail',
            'password': '1234',
            'repeat_password': '1234',
            'email': 0,
            'first_name': '',
            'last_name': '',
            'is_staff': False
        }
        self.invalid_user24_ListEmail = {
            'username': 'TestInvalidEmail',
            'password': '1234',
            'repeat_password': '1234',
            'email': [0, "@gmail.com"],
            'first_name': '',
            'last_name': '',
            'is_staff': False
        }
        self.invalid_user15_NumberFN = {
            'username': 'TestInvalidFName',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': 0,
            'last_name': '',
            'is_staff': False
        }
        self.invalid_user25_ListFN = {
            'username': 'TestInvalidFName',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': [0, "first"],
            'last_name': '',
            'is_staff': False
        }
        self.invalid_user16_NumberLN = {
            'username': 'TestInvalidLName',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': '',
            'last_name': 0,
            'is_staff': False
        }
        self.invalid_user26_ListLN = {
            'username': 'TestInvalidLName',
            'password': '1234',
            'repeat_password': '1234',
            'email': '',
            'first_name': '',
            'last_name': [0, "last"],
            'is_staff': False
        }
        self.invalid_user17_usernameSpace_1 = {
            'username': ' TestInvalidUsername',
            'password': '12534',
            'repeat_password': '1234',
        }
        self.invalid_user18_usernameSpace_2 = {
            'username': 'Test Invalid Username',
            'password': '12534',
            'repeat_password': '1234',
        }
        self.invalid_user19_password_1 = {
            'username': 'TestInvalidPassword1',
            'password': ' ',
            'repeat_password': '',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }
        self.invalid_user20_RepeatPassword_1 = {
            'username': 'TestInvalidRepeatPassword1',
            'password': '1234',
            'repeat_password': ' ',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }
        self.invalid_user21_password_2 = {
            'username': 'TestInvalidPassword2',
            'password': 'whit Spaces ',
            'repeat_password': '1234',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }
        self.invalid_user22_RepeatPassword_2 = {
            'username': 'TestInvalidRepeatPassword2',
            'password': '1234',
            'repeat_password': 'whit Spaces ',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }

        self.invalid_users = [self.invalid_user0_username,
                              self.invalid_user1_emptyUsername,
                              self.invalid_user2_noUsername,
                              self.invalid_user3_emptyPassword,
                              self.invalid_user4_emptyRepeatPassword,
                              self.invalid_user5_noPassword,
                              self.invalid_user6_noRepeatPassword,
                              self.invalid_user7_differentPassword,
                              self.invalid_user8_email_1,
                              self.invalid_user9_email_2,
                              self.invalid_user10_NoneEmail,
                              self.invalid_user11_NoneFN,
                              self.invalid_user12_NoneLN,
                              self.invalid_user13_NumberAvailable,
                              self.invalid_user14_NumberEmail,
                              self.invalid_user15_NumberFN,
                              self.invalid_user16_NumberLN,
                              self.invalid_user17_usernameSpace_1,
                              self.invalid_user18_usernameSpace_2,
                              self.invalid_user19_password_1,
                              self.invalid_user20_RepeatPassword_1,
                              self.invalid_user21_password_2,
                              self.invalid_user22_RepeatPassword_2,
                              self.invalid_user23_ListAvailable,
                              self.invalid_user24_ListEmail,
                              self.invalid_user25_ListFN,
                              self.invalid_user26_ListLN]

    def test_create_invalid_user(self):
        print("#########-Test POST Invalid User-#########")
        response = []
        log_in()

        for i in range(len(self.invalid_users)):
            self.assertTrue(self.client.login(username='admin', password='admin'))

            response.append(self.client.post("http://127.0.0.1:8000/login/users/",
                                             data=json.dumps(self.invalid_users[i]),
                                             content_type='application/json'))

            # print(">I>>", i, response[i].data)     # Debug
            self.assertEqual(response[i].status_code, status.HTTP_409_CONFLICT)


class PutUserTest1(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='TestFullUpdate', email="pepito@kingdom.com",
            password='1234', is_staff=True)

        User.objects.create_user(
            username='TestRestore', email="",
            password='1234', is_staff=True,
            is_active=False)

    def test_valid_update_user_owner(self):
        print("#########-Test Valid PUT Owner-#########")

        self.assertTrue(self.client.login(username='TestFullUpdate', password='1234'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/1/")
        # get data from db
        user = User.objects.get(pk=1)
        serializer = UserSerializer(user)
        # It compares the data of the response with those of the database.
        self.assertEqual(response.data, serializer.data)

        # Put new data
        response = self.client.put("http://127.0.0.1:8000/login/users/1/",
                                   data=json.dumps({
                                       'username': 'TestFullUpdate',
                                       'password': '',
                                       'email': 'pepito@kingdom.com',
                                       'first_name': 'Pepito',
                                       'last_name': 'Grillo',
                                       'is_staff': "faLse",
                                       'is_active': "true"
                                   }),
                                   content_type='application/json')

        # print(">>", response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get data from db
        user_updated = User.objects.get(pk=1)
        serializer_updated = UserSerializer(user_updated)

        # Temporary treatment to check the rest of the data.
        del response.data['token']

        # It compares the data of the response with those of the database.
        self.assertEqual(response.data, serializer_updated.data)  # ['data']
        # compare changes:
        self.assertNotEqual(serializer_updated.data, serializer.data)

    def test_valid_update_user_admin(self):
        print("#########-Test Valid PUT Admin-#########")
        log_in()

        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/1/")
        # get data from db
        user = User.objects.get(pk=1)
        serializer = UserSerializer(user)
        # It compares the data of the response with those of the database.
        self.assertEqual(response.data, serializer.data)

        # Put new data
        response = self.client.put("http://127.0.0.1:8000/login/users/1/",
                                   data=json.dumps({
                                       'username': 'TestFullUpdate',
                                       'password': '',
                                       'email': 'pepito@kingdom.com',
                                       'first_name': 'Pepito',
                                       'last_name': 'Grillo',
                                       'is_staff': "trUe",
                                       'is_active': True
                                   }),
                                   content_type='application/json')

        # print(">>", response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get data from db
        user_updated = User.objects.get(pk=1)
        serializer_updated = UserSerializer(user_updated)

        # Temporary treatment to check the rest of the data.
        del response.data['token']

        # It compares the data of the response with those of the database.
        self.assertEqual(response.data, serializer_updated.data)  # ['data']
        # compare changes:
        self.assertNotEqual(serializer_updated.data, serializer.data)

    def test_user_banned_deleted(self):
        print("#########-Test DELETE Ban/Delete-#########")
        log_in()

        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/1/")
        # get data from db
        user = User.objects.get(pk=1)
        serializer = UserSerializer(user)
        # It compares the data of the response with those of the database.
        self.assertEqual(response.data, serializer.data)

        # Put new data
        response = self.client.put("http://127.0.0.1:8000/login/users/1/",
                                   data=json.dumps({
                                       'username': 'TestFullUpdate',
                                       'password': '',
                                       'email': 'pepito@kingdom.com',
                                       'first_name': 'Pepito',
                                       'last_name': 'Grillo',
                                       'is_staff': "trUe",
                                       'is_active': False
                                   }),
                                   content_type='application/json')

        # print(">>", response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get data from db
        user_updated = User.objects.get(pk=1)
        serializer_updated = UserSerializer(user_updated)

        self.assertEqual(response.data['is_active'], serializer_updated.data['is_active'])
        # compare changes (The user should be marked as inactive, not deleted):
        self.assertNotEqual(serializer_updated.data['is_active'], serializer.data['is_active'])

    def test_user_restore(self):
        print("#########-Test DELETE Ban/Delete-#########")
        log_in()

        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/2/")
        # get data from db
        user = User.objects.get(pk=2)
        serializer = UserSerializer(user)
        # It compares the data of the response with those of the database.
        self.assertEqual(response.data, serializer.data)

        # Put new data
        response = self.client.put("http://127.0.0.1:8000/login/users/2/",
                                   data=json.dumps({
                                       'username': 'TestRestore',
                                       'password': '',
                                       'email': 'TestRestoreTheLight@kingdom.com',
                                       'first_name': 'Pepito',
                                       'last_name': 'Grillo',
                                       'is_staff': "trUe",
                                       'is_active': True
                                   }),
                                   content_type='application/json')

        # print(">>", response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get data from db
        user_updated = User.objects.get(pk=2)
        serializer_updated = UserSerializer(user_updated)

        self.assertEqual(response.data['is_active'], serializer_updated.data['is_active'])
        # compare changes (The user should be marked as inactive, not deleted):
        self.assertNotEqual(serializer_updated.data['is_active'], serializer.data['is_active'])


class PutUserTest2(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='TestFullUpdate', email="",
            password='1234', is_staff=True)

        User.objects.create_user(
            username='TestInvalidUpdate', email="", password='1234')

        User.objects.create_user(
            username='TestPasswordUpdate', email="", password='1234')

        # Invalid
        self.putDataIV_0 = {
            'username': 'TestInvalidUpdate',
            'email': 'pepitoMagic',
            'first_name': '',
            'last_name': '',
            'is_staff': False
        }

        self.putDataIV_1 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': None,
            'last_name': 'Grillo',
            'is_staff': False
        }

        self.putDataIV_2 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': 'Pepito',
            'last_name': None,
            'is_staff': False
        }

        self.putDataIV_3 = {
            'username': 'TestInvalidUpdate',
            'email': None,
            'first_name': 'Pepito',
            'last_name': 'Grillo',
            'is_staff': False
        }

        self.putDataIV_4 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': 'Pepito',
            'last_name': 'Grillo',
            'is_staff': 'Virus'
        }

        self.putDataIV_5 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': 'Pepito',
            'last_name': 'Grillo',
            'is_staff': None
        }

        self.putDataIV_6 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': 'Pepito',
            'last_name': 'Grillo',
            'is_staff': 0
        }
        self.putDataIV_7 = {
            'username': 'TestInvalidUpdate',
            'email': [1234567, "@gmail.com"],
            'first_name': 'Pepito',
            'last_name': 'Grillo',
            'is_staff': False
        }
        self.putDataIV_8 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': 0,
            'last_name': 'Grillo',
            'is_staff': False
        }
        self.putDataIV_9 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': 'Pepito',
            'last_name': 0,
            'is_staff': False
        }
        self.putDataIV_10 = {
            'username': 'Test Invalid Update',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': False
        }
        self.putDataIV_11 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': False,
            'is_active': "Virus_v2"
        }
        self.putDataIV_12 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': False,
            'is_active': None
        }
        self.putDataIV_13 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': False,
            'is_active': 0
        }
        self.putDataIV_14 = {
            'username': '',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': False,
            'is_active': True
        }
        self.putDataIV_15 = {
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': False,
            'is_active': True
        }
        self.putDataIV_16 = {
            'username': None,
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': False,
            'is_active': True
        }
        self.putDataIV_17 = {
            'username': 0,
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': False,
            'is_active': True
        }
        self.putDataIV_18 = {
            'username': 'TestInvalidUpdate',
            'email': 0,
            'first_name': 'Pepito',
            'last_name': 'Grillo',
            'is_staff': False
        }
        self.putDataIV_19 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': 'Pepito',
            'last_name': 'Grillo',
            'is_staff': [0, "false"]
        }
        self.putDataIV_20 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': [0, "first"],
            'last_name': 'Grillo',
            'is_staff': False
        }
        self.putDataIV_21 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': 'Pepito',
            'last_name': [0, "last"],
            'is_staff': False
        }
        self.putDataIV_22 = {
            'username': 'TestInvalidUpdate',
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': False,
            'is_active': [0, "true"]
        }
        self.putDataIV_23 = {
            'username': [0, "username"],
            'email': '',
            'first_name': '',
            'last_name': '',
            'is_staff': False,
            'is_active': True
        }
        self.putDataIV_24 = {
            'username': 'TestInvalidUpdate',
            'email': [0, "@gmail.com"],
            'first_name': 'Pepito',
            'last_name': 'Grillo',
            'is_staff': False
        }

        # Passwords - Valid
        self.putDataV_password_0 = {
            'username': 'TestPasswordUpdate',
            'password': '12345',
            'repeat_password': '12345',
            'old_password': '1234',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }

        self.putDataV_password_1 = {
            'username': 'TestPasswordUpdate',
            'password': '',
            'repeat_password': '',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }

        # Password - Invalid
        self.putDataIV_password_0 = {
            'username': 'TestPasswordUpdate',
            'password': None,
            'repeat_password': '',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }

        # Not passing the password is the same as leaving it blank, so it is valid.
        # self.putDataIV_password_1 = {
        #     'username': 'TestPasswordUpdate',
        #     'email': '',
        #     'first_name': 'pass',
        #     'last_name': 'word',
        #     'is_staff': False
        # }

        self.putDataIV_password_2 = {
            'username': 'TestPasswordUpdate',
            'password': ' ',
            'repeat_password': '',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }

        self.putDataIV_password_3 = {
            'username': 'TestPasswordUpdate',
            'password': 'con Espacios ',
            'repeat_password': '',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }

        self.putDataIV_password_4 = {
            'username': 'TestPasswordUpdate',
            'password': '',
            'repeat_password': None,
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }

        self.putDataIV_password_5 = {
            'username': 'TestPasswordUpdate',
            'password': '',
            'repeat_password': ' ',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }

        self.putDataIV_password_6 = {
            'username': 'TestPasswordUpdate',
            'password': 'con Espacios ',
            'repeat_password': 'whit Spaces ',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }

        self.putDataIV_password_7 = {
            'username': 'TestPasswordUpdate',
            'password': '',
            'repeat_password': 'whit Spaces ',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }

        self.putDataIV_password_8 = {
            'username': 'TestPasswordUpdate',
            'password': '1234',
            'repeat_password': '4321',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }
        self.putDataIV_password_9 = {
            'username': 'TestPasswordUpdate',
            'password': '12345',
            'repeat_password': '12345',
            'old_password': 'pepitoGrilloSeVaDePaseo',
            'email': '',
            'first_name': 'pass',
            'last_name': 'word',
            'is_staff': False
        }

        self.putDataIV = [self.putDataIV_0, self.putDataIV_1,
                          self.putDataIV_2, self.putDataIV_3,
                          self.putDataIV_4, self.putDataIV_5,
                          self.putDataIV_6, self.putDataIV_7,
                          self.putDataIV_8, self.putDataIV_9,
                          self.putDataIV_10, self.putDataIV_11,
                          self.putDataIV_12, self.putDataIV_13,
                          self.putDataIV_14, self.putDataIV_15,
                          self.putDataIV_16, self.putDataIV_17,
                          self.putDataIV_18, self.putDataIV_19,
                          self.putDataIV_20, self.putDataIV_21,
                          self.putDataIV_22, self.putDataIV_23,
                          self.putDataIV_24]

        # self.putDataV = []

        self.putDataIV_password = [self.putDataIV_password_0,
                                   # self.putDataIV_password_1,
                                   self.putDataIV_password_2,
                                   self.putDataIV_password_3,
                                   self.putDataIV_password_4,
                                   self.putDataIV_password_5,
                                   self.putDataIV_password_6,
                                   self.putDataIV_password_7,
                                   self.putDataIV_password_8,
                                   self.putDataIV_password_9]

        self.putDataV_password = [self.putDataV_password_0,
                                  self.putDataV_password_1]

    def test_invalid_update_user_owner(self):
        print("#########-Test Invalid PUT Owner-#########")
        response = []

        self.assertTrue(self.client.login(username='TestInvalidUpdate', password='1234'))

        for i in range(len(self.putDataIV)):
            response.append(self.client.put("http://127.0.0.1:8000/login/users/2/",
                                            data=json.dumps(self.putDataIV[i]),
                                            content_type='application/json'))

            # print(">><", i, response[i].data)  # Debug
            self.assertEqual(response[i].status_code, status.HTTP_409_CONFLICT)

            # It check if put return a specific error string.
            self.assertEqual(type(response[i].data), type("String"))

    def test_password_update_user_owner(self):
        print("#########-Test Password PUT Owner-#########")
        response_iv = []
        response_v = []

        self.assertTrue(self.client.login(username='TestPasswordUpdate', password='1234'))

        # Invalid
        for i in range(len(self.putDataIV_password)):
            response_iv.append(self.client.put("http://127.0.0.1:8000/login/users/3/",
                                               data=json.dumps(self.putDataIV_password[i]),
                                               content_type='application/json'))

            # print(">>Pass>>", i, response_iv[i].data)   # Debug
            self.assertEqual(response_iv[i].status_code, status.HTTP_409_CONFLICT)

        # Valid
        for i in range(len(self.putDataV_password)):
            response_v.append(self.client.put("http://127.0.0.1:8000/login/users/3/",
                                              data=json.dumps(self.putDataV_password[i]),
                                              content_type='application/json'))

            self.assertTrue(self.client.login(username='TestPasswordUpdate',
                                              password='12345'))

            # print(">>", i, response_v[i].data)  # Debug
            self.assertEqual(response_v[i].status_code, status.HTTP_200_OK)

    def test_password_update_user_admin(self):
        print("#########-Test Password PUT Admin-#########")
        response_v = []
        log_in()

        for i in range(len(self.putDataV_password)):
            self.assertTrue(self.client.login(username='admin', password='admin'))

            response_v.append(self.client.put("http://127.0.0.1:8000/login/users/3/",
                                              data=json.dumps(self.putDataV_password[i]),
                                              content_type='application/json'))

            # print(">>", i, response_v[i].data)  # Debug

            self.assertTrue(self.client.login(username='TestPasswordUpdate',
                                              password='12345'))

            self.assertEqual(response_v[i].status_code, status.HTTP_200_OK)


class DeleteUserTest(APITestCase):
    global json_data

    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            email="",
            password="user1"
        )
        self.user.save()

        self.user2 = User.objects.create_user(
            username="user2",
            email="",
            password="user2"
        )
        self.user2.save()

        self.user3 = User.objects.create_user(
            username="user3",
            email="",
            password="user3"
        )
        self.user3.save()

        self.user4 = User.objects.create_user(
            username="user4",
            email="",
            password="user4",
            is_active=False
        )
        self.user4.save()

        self.book = Book()
        self.book.edit_book(title=json_data['Title'], description="", author=json_data['Authors'][0],
                            editorial=json_data['Publisher'], language=json_data['Language'],
                            isbn="978-3-16-148410-0", user=self.user3)

        self.history = History()

    def test_delete_user(self):
        print("#########-Test DELETE Ban/Delete-#########")
        log_in()

        self.assertTrue(self.client.login(username='admin', password='admin'))

        # get API response
        response = self.client.get("http://127.0.0.1:8000/login/users/2/")
        # get data from db
        user = User.objects.get(pk=2)
        serializer = UserSerializer(user)
        # It compares the data of the response with those of the database.
        self.assertEqual(response.data, serializer.data)

        # Put new data
        response = self.client.delete("http://127.0.0.1:8000/login/users/2/")

        # print(">>", response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get data from db
        user_updated = User.objects.get(pk=2)
        serializer_updated = UserSerializer(user_updated)

        self.assertEqual(response.data, None)
        # compare changes (The user should be marked as inactive, not deleted):
        self.assertNotEqual(serializer_updated.data['is_active'], serializer.data['is_active'])

    def test_delete_user_UnLogged(self):
        print("#########-Test DELETE User UnLogged-#########")

        user_pk = self.user.pk

        response = self.client.delete("http://127.0.0.1:8000/login/users/{pk}/"
                                      .format(pk=user_pk),
                                      content_type='application/json')

        # print("<<D>>", response.data)   # Debug

        response = self.client.get("http://127.0.0.1:8000/login/users/{pk}/"
                                   .format(pk=user_pk),
                                   content_type='application/json')

        # print("<<D-G>>", response.data)  # Debug

        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_noStaff(self):
        print("#########-Test DELETE User NoStaff-#########")

        self.assertTrue(self.client.login(username='user2', password='user2'))

        user_pk = self.user.pk

        response = self.client.delete("http://127.0.0.1:8000/login/users/{pk}/"
                                      .format(pk=user_pk),
                                      content_type='application/json')

        # print("<<D>>", response.data)  # Debug

        response = self.client.get("http://127.0.0.1:8000/login/users/{pk}/"
                                   .format(pk=user_pk),
                                   content_type='application/json')

        # print("<<D-G>>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_with_book_rented(self):
        print("#########-Test DELETE User With Book Rented-#########")
        log_in()

        self.assertTrue(self.client.login(username='admin', password='admin'))

        user_pk = self.user.pk

        # Rent book to user.
        response_rent = self.client.post("http://127.0.0.1:8000/library/history/",
                                         data=json.dumps({
                                             'uuid_book': str(self.book.uuid_book),
                                             'pk': self.user.pk
                                         }),
                                         content_type='application/json')

        self.assertEqual(response_rent.status_code, status.HTTP_201_CREATED)

        response = self.client.delete("http://127.0.0.1:8000/login/users/{pk}/"
                                      .format(pk=user_pk),
                                      content_type='application/json')

        # print("<<DUBR>>", response.data)   # Debug

        response = self.client.get("http://127.0.0.1:8000/login/users/{pk}/"
                                   .format(pk=user_pk),
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['is_active'], False)

        response = self.client.get("http://127.0.0.1:8000/library/history/{uuid}/"
                                   .format(uuid=response_rent.data['uuid_loan']),
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_deleted_user(self):
        print("#########-Test Get Deleted User-#########")
        log_in()

        # Admin
        self.assertTrue(self.client.login(username='admin', password='admin'))

        response = self.client.get("http://127.0.0.1:8000/login/users/4/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LoginUserTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            email="",
            password="user1",
            is_active=False
        )
        self.user.save()

        self.user2 = User.objects.create_user(
            username="user2",
            email="test@drf.com",
            password="user2"
        )

    def test_valid_login_user_username(self):
        print("#########-Test valid LOGIN User-#########")
        log_in()

        response = self.client.post("http://127.0.0.1:8000/login/setLogin/",
                                    data=json.dumps({
                                        'username': "admin",
                                        'password': "admin"
                                    }),
                                    content_type='application/json')

        # print("<<L>>", response.data)   # Debug
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        aux_user = User.objects.get(username=response.data['username'])
        token, _ = Token.objects.get_or_create(user=aux_user)
        user = UserSerializer(aux_user).data
        user['token'] = token.key

        self.assertEqual(response.data, user)

        response = self.client.post("http://127.0.0.1:8000/login/logOut/",
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post("http://127.0.0.1:8000/login/users/",
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_login_user_email(self):
        print("#########-Test valid LOGIN User-#########")
        response = self.client.post("http://127.0.0.1:8000/login/setLogin/",
                                    data=json.dumps({
                                        'username': "test@drf.com",
                                        'password': "user2"
                                    }),
                                    content_type='application/json')

        # print("<<L>>", response.data)   # Debug
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        aux_user = User.objects.get(email=response.data['email'])
        token, _ = Token.objects.get_or_create(user=aux_user)
        user = UserSerializer(aux_user).data
        user['token'] = token.key

        self.assertEqual(response.data, user)

        response = self.client.post("http://127.0.0.1:8000/login/logOut/",
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post("http://127.0.0.1:8000/login/users/",
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_login_user(self):
        print("#########-Test invalid LOGIN User-#########")
        log_in()

        response = self.client.post("http://127.0.0.1:8000/login/setLogin/",
                                    data=json.dumps({
                                        'username': "admin",
                                        'password': "dmin"
                                    }),
                                    content_type='application/json')

        # print("<<L>>", response.data)   # Debug

        user = User.objects.get(username='admin')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # It compares the data of the response with those of the database.
        self.assertNotEqual(response.data, UserSerializer(user).data)

        response = self.client.get("http://127.0.0.1:8000/login/users/",
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonActive_user(self):
        print("#########-Test invalid LOGIN User-#########")
        response = self.client.post("http://127.0.0.1:8000/login/setLogin/",
                                    data=json.dumps({
                                        'username': self.user.username,
                                        'password': "user1"
                                    }),
                                    content_type='application/json')

        # print("<<L>>", response.data)   # Debug

        user = User.objects.get(username='user1')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        self.assertEqual(response.data, "User is disabled.")

        # It compares the data of the response with those of the database.
        self.assertNotEqual(response.data, UserSerializer(user).data)

        response = self.client.get("http://127.0.0.1:8000/login/users/",
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_login_user_username(self):
        print("#########-Test Invalid LOGIN User username-#########")
        response = self.client.post("http://127.0.0.1:8000/login/setLogin/",
                                    data=json.dumps({
                                        'username': "pepito",
                                        'password': "grillo"
                                    }),
                                    content_type='application/json')

        # print("<<iL>>", response.data)   # Debug
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_invalid_login_user_email(self):
        print("#########-Test Invalid LOGIN User email-#########")
        response = self.client.post("http://127.0.0.1:8000/login/setLogin/",
                                    data=json.dumps({
                                        'username': "UnRegistered@drf.com",
                                        'password': "ahhhff"
                                    }),
                                    content_type='application/json')

        # print("<<iL>>", response.data)   # Debug
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class ForgottenPasswordTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1",
                                             email="test@test.com",
                                             password="1234")

        self.user2 = User.objects.create_user(username="user2",
                                              email="test2@test.com",
                                              password="1234",
                                              is_active=False)

    def test_reset_password(self):
        print("#########-Test Reset User Password-#########")

        self.assertTrue(self.client.login(username="user1", password="1234"))
        self.client.logout()

        response = self.client.post("http://127.0.0.1:8000/login/forgotten/",
                                    data=json.dumps({
                                        'username': "test@test.com"
                                    }),
                                    content_type='application/json')

        # print("<<RP>>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        uid, token = response.data['uid'], response.data['token']

        response = self.client.post("http://127.0.0.1:8000/login/changePassword/{}/{}/"
                                    .format(uid, token),
                                    data=json.dumps({
                                        'password': "user1"
                                    }),
                                    content_type='application/json')

        # print("<<RP>>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(self.client.login(username="user1", password="user1"))
        self.client.logout()

    def test_reset_password_invalid_email(self):
        print("#########-Test Invalid Reset User Password-#########")

        self.assertTrue(self.client.login(username="user1", password="1234"))
        self.client.logout()

        response = self.client.post("http://127.0.0.1:8000/login/forgotten/",
                                    data=json.dumps({
                                        'username': "test@"
                                    }),
                                    content_type='application/json')

        # print("<<RP>>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_reset_password_deleted_user(self):
        print("#########-Test Invalid Reset User Password-#########")

        self.assertFalse(self.client.login(username="user2", password="1234"))

        response = self.client.post("http://127.0.0.1:8000/login/forgotten/",
                                    data=json.dumps({
                                        'username': "test2@test.com"
                                    }),
                                    content_type='application/json')

        # print("<<RP>>", response.data)  # Debug

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
