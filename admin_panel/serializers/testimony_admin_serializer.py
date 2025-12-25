from rest_framework import serializers
from contents.models.testimony import Testimony

class AdminTestimonySerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source="member.first_name", read_only=True)
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()

    class Meta:
        model = Testimony
        fields = [
            "id",
            "text",
            "images",        # now returns list of images
            "videos",        # now returns list of videos
            "member_name",
            "status",
            "rejection_reason",
            "created_at",
        ]

    def get_images(self, obj):
        """
        Return list of images with their ID and URL.
        """
        return [{"id": img.id, "url": img.image.url} for img in obj.images.all()]

    def get_videos(self, obj):
        """
        Return list of videos with their ID and URL.
        """
        return [{"id": vid.id, "url": vid.video.url} for vid in obj.videos.all()]
