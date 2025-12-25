from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# contents/models/event.py

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="events/images/")
    def __str__(self):
        return f"Image for {self.event.title}"

class EventVideo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="events/videos/")
    def __str__(self):
        return f"Image for {self.event.title}"
