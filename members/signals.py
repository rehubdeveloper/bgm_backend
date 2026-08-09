from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from .models import Member

member_registered = Signal()
member_updated = Signal()

@receiver(post_save, sender=Member)
def broadcast_member_events(sender, instance, created, **kwargs):
    if created:
        member_registered.send(sender=sender, member=instance, created=True)
    else:
        member_updated.send(sender=sender, member=instance, updated_fields=None)
