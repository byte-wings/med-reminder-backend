from django.test import TestCase
from asgiref.sync import async_to_sync
from rest_framework.test import APIClient
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

from .models import Reminder

User = get_user_model()


class ReminderTestCase(TestCase):
    """Test case for the Reminder model"""

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
        self.reminder = Reminder.objects.create(
            user=self.user,
            medication_name='Test Medication',
            dosage='1 pill',
            time='2022-01-01T00:00:00Z',
            is_active=True
        )

    def test_reminder_creation(self):
        """Test the creation of a reminder"""
        self.assertEqual(self.reminder.medication_name, 'Test Medication')
        self.assertEqual(self.reminder.dosage, '1 pill')
        self.assertEqual(self.reminder.is_active, True)

    def test_send_notification(self):
        """Test the send_notification method"""
        channel_layer = get_channel_layer()
        message = {
            'type': 'send_notification',
            'message': f'Time to take your medication: {self.reminder.medication_name}, Dosage: {self.reminder.dosage}'
        }
        async_to_sync(channel_layer.group_send)(
            f'notifications_{self.user.id}',
            message
        )
        self.assertEqual(self.reminder.is_active, False)
