from rest_framework import serializers
from contents.models.devotional import DailyDevotional


class DailyDevotionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyDevotional
        fields = "__all__"
