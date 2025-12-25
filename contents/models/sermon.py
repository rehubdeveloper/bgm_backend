# contents/models/sermon.py
from django.db import models

class Sermon(models.Model):
    title = models.CharField(max_length=255)
    preacher = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SermonAudio(models.Model):
    sermon = models.ForeignKey(Sermon, on_delete=models.CASCADE, related_name="audios")
    audio = models.FileField(upload_to="sermons/audio/")
