from django.db import models
from django.utils import timezone

class OutboundMessage(models.Model):
    channel = models.CharField(max_length=20, choices=[('email','Email'),('whatsapp','WhatsApp')])
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    html_body = models.TextField(blank=True, null=True)
    recipients = models.JSONField(default=list)
    related_type = models.CharField(max_length=100, blank=True, null=True)
    related_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    attempts = models.IntegerField(default=0)
    last_error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(blank=True, null=True)

class MessageLog(models.Model):
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

class MessageTemplate(models.Model):
    key = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=255)
    html = models.TextField()
    plaintext = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
