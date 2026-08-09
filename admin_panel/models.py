from django.db import models
from django.conf import settings
from django.utils import timezone

class Role(models.Model):
    ROLE_CHOICES = [('superadmin','Super Admin'),('branch_admin','Branch Admin'),('media_manager','Media Manager'),('finance','Finance')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_role')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.email} ({self.get_role_display()})"

class AdminActionLog(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='admin_actions')
    action = models.CharField(max_length=255)
    target_type = models.CharField(max_length=100, blank=True, null=True)
    target_id = models.IntegerField(blank=True, null=True)
    details = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.action} by {self.actor}"
