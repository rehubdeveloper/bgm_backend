from rest_framework import serializers
from messaging.models.message_log import MessageLog

class MessageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageLog
        fields = "__all__"
