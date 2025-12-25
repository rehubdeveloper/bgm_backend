# contents/serializers/sermon_serializers.py
from rest_framework import serializers
from contents.models.sermon import Sermon, SermonAudio

class SermonAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = SermonAudio
        fields = ["id", "audio"]

class SermonSerializer(serializers.ModelSerializer):
    audios = SermonAudioSerializer(many=True, read_only=True)

    class Meta:
        model = Sermon
        fields = ["id", "title", "preacher", "description", "created_at", "audios"]
