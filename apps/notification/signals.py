from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Reminder


@receiver(post_save, sender=Reminder)
def trigger_reminder_notification(sender, instance, created, **kwargs):
    if created and instance.is_active:
        instance.send_notification()

    # You can also add a check for when the reminder time is due
    if instance.time <= timezone.now() and instance.is_active:
        instance.send_notification()
        instance.is_active = False
        instance.save()
