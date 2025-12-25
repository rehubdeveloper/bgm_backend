from rest_framework import serializers
from contents.models.event import Event, EventImage, EventVideo

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ["id", "image"]

class EventVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventVideo
        fields = ["id", "video"]

class EventSerializer(serializers.ModelSerializer):
    images = EventImageSerializer(many=True, read_only=True)
    videos = EventVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "description", "event_date", "images", "videos", "created_at"]