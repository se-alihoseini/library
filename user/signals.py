from user.models import User, Subscription

from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(signal=post_save, sender=User)
def create_subscription(sender, **kwargs):
    Subscription.objects.create(user=kwargs['instance'])
