# contents/serializers/testimony_serializers.py
from rest_framework import serializers
from contents.models.testimony import Testimony, TestimonyImage, TestimonyVideo

class TestimonyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestimonyImage
        fields = ["id", "image"]

class TestimonyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestimonyVideo
        fields = ["id", "video"]

class TestimonySerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source="member.first_name", read_only=True)
    images = TestimonyImageSerializer(many=True, read_only=True)
    videos = TestimonyVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Testimony
        fields = [
            "id",
            "text",
            "member_name",
            "status",
            "rejection_reason",
            "images",
            "videos",
            "created_at"
        ]
        read_only_fields = ["id", "member_name", "status", "rejection_reason", "created_at"]
