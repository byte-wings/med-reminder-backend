from django.db import models
from django.utils import timezone
from django.conf import settings


class Reminder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.medication_name} for {self.user.username} at {self.time}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_active and self.time <= timezone.now():
            self.send_notification()

    def send_notification(self):
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        import json

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{self.user.id}',
            {
                'type': 'send_notification',
                'message': f'Time to take your medication: {self.medication_name}, Dosage: {self.dosage}'
            }
        )
        self.is_active = False
        self.save()
