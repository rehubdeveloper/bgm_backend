# contents/models/about.py
from django.db import models

class About(models.Model):
    ABOUT_TYPE_CHOICES = [
        ("church", "About Church"),
        ("pastor", "About Pastor"),
    ]

    type = models.CharField(max_length=20, choices=ABOUT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()}"

class AboutImage(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="about/")

    def __str__(self):
        return f"Image for {self.about.title}"
