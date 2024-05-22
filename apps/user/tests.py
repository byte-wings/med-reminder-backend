from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import User
from .serializers import UserSerializer, UserUpdateSerializer


class UserTestCase(TestCase):
    """Test case for the User model"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            phone_number='998998887766',
            password='testpassword',
            first_name='Test',
            last_name='User',
            gender='male',
            email='testuser@gmail.com',
            birth_date='1990-01-01'
        )

    def test_user_detail_view(self):
        """Test the user detail view"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('user-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, UserSerializer(self.user).data)

    def test_user_update_view(self):
        """Test the user update view"""
        self.client.force_authenticate(user=self.user)
        new_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'gender': 'female',
            'email': 'updateduser@gmail.com',
            'birth_date': '1991-01-01'
        }
        response = self.client.patch(reverse('user-update'), new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(UserSerializer(self.user).data, response.data)
