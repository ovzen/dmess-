# Create your tests here.
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


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
        url_valid = reverse('invite-detail', kwargs={'pk': '9a46812a-b0e8-44b0-b1cd-021a84aba71f'})
        url_invalid = reverse('invite-detail', kwargs={'pk': '5d34c8fc97b6414eb42052d2fb525abc'})
        response_1 = self.client.get(url_valid, format='json', )
        response_2 = self.client.get(url_invalid, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_invite(self):
        url_valid = reverse('invite-detail', kwargs={'pk': '9a46812a-b0e8-44b0-b1cd-021a84aba71f'})
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

    def test_get_registers(self):
        url = reverse('register-stat')
        response = self.client.get(url, format='json')
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
