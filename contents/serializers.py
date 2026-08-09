from rest_framework import serializers
from .models import About, DailyDevotional, Testimony, Event, Sermon

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'

class DailyDevotionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyDevotional
        fields = '__all__'

class TestimonySerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimony
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class SermonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sermon
        fields = '__all__'
