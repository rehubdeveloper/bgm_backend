from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from members.models.member import Member

# Custom signals (no providing_args in Django 4+)
member_registered = Signal()
member_updated = Signal()

@receiver(post_save, sender=Member)
def broadcast_member_events(sender, instance: Member, created, update_fields=None, **kwargs):
    """
    Emit custom signals for other apps (messaging) to pick up.
    """
    if created:
        # New member created
        member_registered.send(sender=sender, member=instance, created=True)
    else:
        # Member updated
        member_updated.send(sender=sender, member=instance, updated_fields=update_fields)
