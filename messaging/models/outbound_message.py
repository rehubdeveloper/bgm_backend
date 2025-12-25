from django.db import models
from django.utils import timezone

CHANNEL_CHOICES = [
    ("email", "Email"),
    ("whatsapp", "WhatsApp"),
]

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("sent", "Sent"),
    ("failed", "Failed"),
]

class OutboundMessage(models.Model):
    """
    Represents a queued outbound message (email / whatsapp) that can be retried.
    """
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)      # plain/text fallback
    html_body = models.TextField(blank=True, null=True) # HTML for email
    recipients = models.JSONField(default=list)         # list of emails or phone numbers
    related_type = models.CharField(max_length=100, blank=True, null=True) # e.g. "devotional"
    related_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    attempts = models.IntegerField(default=0)
    last_error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
