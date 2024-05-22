from django.db import models

from apps.notification.consumers import User


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
    ethnicity = models.TextField()


