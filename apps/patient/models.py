from django.db import models
from django.utils import timezone

from apps.notification.consumers import User


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
    ethnicity = models.TextField()


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    doctor = models.CharField(max_length=150)
    notes = models.TextField()


class Drugs(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    amount = models.FloatField()

    notes = models.TextField()
