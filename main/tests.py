"""Пример написания тестов для API сайта

- Написание тестов: https://www.django-rest-framework.org/api-guide/testing/
- Авторизация: https://www.django-rest-framework.org/api-guide/testing/#authenticating

"""
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import json
import unittest

from main.models import UserProfile, Contact, Message


class DialogTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_get_dialogs_list(self):
        url = reverse('dialog-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_dialog(self):
        url = reverse('dialog-list')
        data = {
            'name': 'test',
            'users': [1, 3]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_dialog(self):
        url_valid = reverse('dialog-detail', kwargs={'pk': '644804bf-13c9-47d4-b70b-a9b95f44b7b4'})
        url_invalid = reverse('dialog-detail', kwargs={'pk': '56989add477e45358b344cc25842955c'})
        response_1 = self.client.get(url_valid, format='json')
        response_2 = self.client.get(url_invalid, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_dialog(self):
        url_valid = reverse('dialog-detail', kwargs={'pk': '644804bf-13c9-47d4-b70b-a9b95f44b7b4'})
        url_invalid = reverse('dialog-detail', kwargs={'pk': '56989add477e45358b344cc25842955c'})
        response_1 = self.client.delete(url_valid, format='json')
        response_2 = self.client.delete(url_invalid, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)

    # def test_read_messages(self):
    #     url = reverse('dialog-detail', kwargs={'pk': '644804bf-13c9-47d4-b70b-a9b95f44b7b4'}) + 'read_messages/'
    #     response = self.client.post(url, format='json')
    #     self.assertEqual(Message.objects.filter(user=2, dialog='644804bf-13c9-47d4-b70b-a9b95f44b7b4').first().is_read, True)


class MessageTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_get_messages_list(self):
        url = reverse('message-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_message(self):
        url = reverse('message-list')
        data = {
            'text': 'test',
            'user': 1,
            'dialog': '644804bf-13c9-47d4-b70b-a9b95f44b7b4'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_get_message(self):
    #     url_valid = reverse('message-detail', kwargs={'pk': 1})
    #     url_invalid = reverse('message-detail', kwargs={'pk': 42})
    #     response_1 = self.client.get(url_valid, format='json')
    #     response_2 = self.client.get(url_invalid, format='json')
    #     self.assertEqual(response_1.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)

    # def test_delete_message(self):
    #     url_valid = reverse('message-detail', kwargs={'pk': 1})
    #     url_invalid = reverse('message-detail', kwargs={'pk': 42})
    #     response_1 = self.client.delete(url_valid, format='json')
    #     response_2 = self.client.delete(url_invalid, format='json')
    #     self.assertEqual(response_1.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)


class ContactTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_get_contacts_list(self):
        url = reverse('contact-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_contact(self):
        url = reverse('contact-list')
        data = {
            'user': 2,
            'contact': 1
        }
        response_1 = self.client.post(url, data, format='json')
        response_2 = self.client.post(url, data, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_contact(self):
        url_valid = reverse('contact-detail', kwargs={'pk': 1})
        url_invalid = reverse('contact-detail', kwargs={'pk': 42})
        response_1 = self.client.get(url_valid, format='json')
        response_2 = self.client.get(url_invalid, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_contact(self):
        url_valid = reverse('contact-detail', kwargs={'pk': 1})
        url_invalid = reverse('contact-detail', kwargs={'pk': 42})
        response_1 = self.client.delete(url_valid, format='json')
        response_2 = self.client.delete(url_invalid, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)


class UserTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_get_users_list(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        url_valid = reverse('user-detail', kwargs={'pk': 1})
        url_invalid = reverse('user-detail', kwargs={'pk': 42})
        response_1 = self.client.get(url_valid, format='json')
        response_2 = self.client.get(url_invalid, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        url_valid = reverse('user-detail', kwargs={'pk': 1})
        url_invalid = reverse('user-detail', kwargs={'pk': 42})
        response_1 = self.client.delete(url_valid, format='json')
        response_2 = self.client.delete(url_invalid, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)

    def test_count_users(self):
        url = reverse('user-count')
        response = self.client.get(url, format='json')
        count = json.loads(response.content)['count']
        self.assertEqual(count, 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_contact(self):
        url = reverse('user-detail', kwargs={'pk': 3}) + 'add_contact/'
        response = self.client.post(url, 1, format='json')
        self.assertEqual(Contact.objects.filter(user=1, contact=3).exists(), True)

    def test_update_user(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        data['username'] = 'something'
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserProfileCreationTestCase(unittest.TestCase):
    def test_user_profile_creation(self):
        user = User.objects.create_user('Test', 'pascal@abc.net', 'ytrewq123')
        is_user_profile_exists = UserProfile.objects.filter(user=user).exists()
        self.assertEqual(is_user_profile_exists, True)


class UserInviteProcessingTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_invite_processing(self):
        url = '/api/accounts/register/?invite_code=6c39d935-11f3-4031-a407-2366443b55b4'
        data = {
            'username': 'Test',
            'password': 'ytrewq123',
            'email': 'pascal@abc.net'
        }
        response = self.client.post(url, data, format='json')
        user = User.objects.get(username='Test')
        self.assertEqual(user.is_staff, True)

    def test_used_invite_processing(self):
        url = '/api/accounts/register/?invite_code=ef5c2c0c-3ffa-4dd0-9b4f-9e5d425b3b2e'
        data = {
            'username': 'Test',
            'password': 'ytrewq123',
            'email': 'pascal@abc.net'
        }
        response = self.client.post(url, data, format='json')
        user = User.objects.get(username='Test')
        self.assertEqual(user.is_staff, False)

    def test_nonexistent_invite_processing(self):
        url = '/api/accounts/register/?invite_code=77731fdc-4970-4cc5-b8e9-f99d7b029777'
        data = {
            'username': 'Test',
            'password': 'ytrewq123',
            'email': 'pascal@abc.net'
        }
        response = self.client.post(url, data, format='json')
        user = User.objects.get(username='Test')
        self.assertEqual(user.is_staff, False)
