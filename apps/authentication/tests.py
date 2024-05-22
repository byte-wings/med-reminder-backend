from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserConfirmation, ConfirmationRefreshToken

User = get_user_model()


class AuthenticationTestCase(TestCase):
    """Test case for the Authentication models"""

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
        self.confirmation = UserConfirmation.objects.create(
            code='123456',
            user=self.user,
            is_confirmed=False
        )
        self.refresh_token = ConfirmationRefreshToken.objects.create(
            user=self.user,
            token=str(RefreshToken.for_user(self.user)),
            refresh_count=0,
            max_refresh=3
        )

    def test_user_confirmation_creation(self):
        """Test the creation of a user confirmation"""
        self.assertEqual(self.confirmation.code, '123456')
        self.assertEqual(self.confirmation.is_confirmed, False)

    def test_confirmation_refresh_token_creation(self):
        """Test the creation of a confirmation refresh token"""
        self.assertEqual(self.refresh_token.refresh_count, 0)
        self.assertEqual(self.refresh_token.max_refresh, 3)
        self.assertEqual(self.refresh_token.is_refreshable(), True)
