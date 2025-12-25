from django.db import models

class MessageTemplate(models.Model):
    """
    Optional templates stored in DB. You can also use filesystem templates in messaging/templates/.
    """
    key = models.CharField(max_length=100, unique=True)  # e.g. 'devotional_notification'
    subject = models.CharField(max_length=255)
    html = models.TextField()
    plaintext = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
