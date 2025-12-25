# contents/models/testimony.py
from django.db import models
from members.models.member import Member

class Testimony(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    text = models.TextField()

    APPROVAL_STATES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(max_length=20, choices=APPROVAL_STATES, default="pending")
    rejection_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimony from {self.member.first_name if self.member else 'Anonymous'}"

class TestimonyImage(models.Model):
    testimony = models.ForeignKey(Testimony, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="testimonies/images/")

class TestimonyVideo(models.Model):
    testimony = models.ForeignKey(Testimony, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="testimonies/videos/")
