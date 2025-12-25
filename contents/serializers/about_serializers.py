# contents/serializers/about_serializers.py
from rest_framework import serializers
from contents.models.about import About, AboutImage

class AboutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutImage
        fields = ["id", "image"]

class AboutSerializer(serializers.ModelSerializer):
    images = AboutImageSerializer(many=True, read_only=True)

    class Meta:
        model = About
        fields = ["id", "type", "title", "content", "images", "updated_at"]
