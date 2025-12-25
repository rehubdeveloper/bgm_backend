from django.db import models


class DailyDevotional(models.Model):
    title = models.CharField(max_length=255)
    bible_verse = models.CharField(max_length=255)
    reflection = models.TextField()
    prayer = models.TextField()
    application_tip = models.TextField()
    closing_thought = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
