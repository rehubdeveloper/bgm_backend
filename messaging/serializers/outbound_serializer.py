from rest_framework import serializers
from messaging.models.outbound_message import OutboundMessage

class OutboundMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutboundMessage
        fields = "__all__"
        read_only_fields = ("status", "attempts", "last_error", "created_at", "sent_at")
