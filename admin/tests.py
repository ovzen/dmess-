# Create your tests here.
from datetime import datetime

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
import json

from main.models import UserProfile

User = get_user_model()


class InviteTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_get_invites_list(self):
        url = reverse('invite-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invite(self):
        url = reverse('invite-list')
        data = {
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_invite(self):
        url_valid = reverse('invite-detail', kwargs={'pk': '901dd0e8-2453-4a47-b449-032935bdf8b3'})
        url_invalid = reverse('invite-detail', kwargs={'pk': '5d34c8fc97b6414eb42052d2fb525abc'})
        response_1 = self.client.get(url_valid, format='json', )
        response_2 = self.client.get(url_invalid, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_invite(self):
        url_valid = reverse('invite-detail', kwargs={'pk': '901dd0e8-2453-4a47-b449-032935bdf8b3'})
        url_invalid = reverse('invite-detail', kwargs={'pk': '7fc9cbe7a49c422fa15e8c218822dfe0'})
        response_1 = self.client.delete(url_valid, format='json')
        response_2 = self.client.delete(url_invalid, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)


class RegisterStatTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_get_registers_without_date(self):
        url = reverse('register-stat')
        response = self.client.get(url, format='json')
        count = json.loads(response.content)['count']
        self.assertEqual(count, User.objects.filter(date_joined__startswith=datetime.now().date()).count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_registers_with_date(self):
        url = reverse('register-stat')
        response = self.client.get(url, format='json', data={'date': '2020-05-14'})
        count = json.loads(response.content)['count']
        self.assertEqual(count, User.objects.filter(date_joined__startswith='2020-05-14').count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserStatTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_get_online(self):
        url = reverse('user-stat')
        response = self.client.get(url, format='json')
        count = json.loads(response.content)['count']
        self.assertEqual(count, UserProfile.objects.filter(is_online=True).count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GitlabMetricsTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        user = User.objects.get(id=1)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_get_gitlab_metrics(self):
        url = reverse('gitlabmetrics')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
