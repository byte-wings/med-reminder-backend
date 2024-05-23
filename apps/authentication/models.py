from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class ConfirmationRefreshToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    refresh_count = models.IntegerField(default=0)
    max_refresh = models.IntegerField(default=3)

    def save(self, *args, **kwargs):
        if self.is_refreshable():
            self.refresh_count += 1
        super().save(*args, **kwargs)

    def is_refreshable(self):
        return self.refresh_count < self.max_refresh


class UserConfirmation(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiration_time = timezone.now() + timedelta(minutes=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)
