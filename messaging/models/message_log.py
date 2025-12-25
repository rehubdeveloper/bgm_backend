from django.db import models
from django.utils import timezone

class MessageLog(models.Model):
    """
    Keeps a history of message send attempts (both success and failure).
    """
    channel = models.CharField(max_length=20)
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    html_body = models.TextField(blank=True, null=True)
    recipient = models.CharField(max_length=255)
    related_type = models.CharField(max_length=100, blank=True, null=True)
    related_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
