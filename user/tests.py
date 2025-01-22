from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.models import CustomUser
from user.serializers import UserSerializer

class CustomUserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpass123'
        }
        self.user = CustomUser.objects.create_user(
            username='existinguser',
            email='existing@test.com',
            password='existing123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        """Test creating a new user"""
        url = reverse('user-list-create')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(username='testuser').email, 'test@test.com')

    def test_get_users_list(self):
        """Test retrieving users list"""
        url = reverse('user-list-create')
        response = self.client.get(url)
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_user_detail(self):
        """Test retrieving user detail"""
        url = reverse('user-retrieve-update-destroy', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user(self):
        """Test updating user"""
        url = reverse('user-retrieve-update-destroy', kwargs={'pk': self.user.pk})
        update_data = {
            'email': 'updated@test.com'
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@test.com')

    def test_delete_user(self):
        """Test deleting user"""
        url = reverse('user-retrieve-update-destroy', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_unauthorized_update(self):
        """Test unauthorized user update attempt"""
        other_user = CustomUser.objects.create_user(
            username='otheruser',
            email='other@test.com',
            password='other123'
        )
        url = reverse('user-retrieve-update-destroy', kwargs={'pk': other_user.pk})
        update_data = {'email': 'hacked@test.com'}
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete(self):
        """Test unauthorized user deletion attempt"""
        other_user = CustomUser.objects.create_user(
            username='otheruser',
            email='other@test.com',
            password='other123'
        )
        url = reverse('user-retrieve-update-destroy', kwargs={'pk': other_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)