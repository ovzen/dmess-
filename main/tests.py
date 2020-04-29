"""Пример написания тестов для API сайта

- Написание тестов: https://www.django-rest-framework.org/api-guide/testing/
- Авторизация: https://www.django-rest-framework.org/api-guide/testing/#authenticating

"""
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from main.models import Contact, Dialog, Message


class WikiTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_create_wikipage(self):
        url = reverse('wiki-list')
        data = {
            'title': 'Hello',
            'text_markdown': '> Hi\nthis is *markdown text*',
            'dialog': 1,
            'message': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ContactTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        user = User.objects.get(id=1)
        user1 = User.objects.get(id=2)
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        Contact.objects.create(user=user, contact=user1)

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
