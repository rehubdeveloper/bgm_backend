from django.db import models

class About(models.Model):
    ABOUT_TYPE_CHOICES = [('church','About Church'),('pastor','About Pastor')]
    type = models.CharField(max_length=20, choices=ABOUT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='about/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"

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

class Testimony(models.Model):
    member = models.ForeignKey('members.Member', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    image = models.ImageField(upload_to='testimonies/images/', null=True, blank=True)
    video = models.FileField(upload_to='testimonies/videos/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Testimony {self.id}"

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    images = models.JSONField(default=list, blank=True)
    videos = models.JSONField(default=list, blank=True)
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Sermon(models.Model):
    title = models.CharField(max_length=255)
    preacher = models.CharField(max_length=255, null=True, blank=True)
    audio = models.FileField(upload_to='sermons/audio/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
