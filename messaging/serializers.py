from rest_framework import serializers
from .models import OutboundMessage, MessageLog, MessageTemplate

class OutboundMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutboundMessage
        fields = '__all__'
        read_only_fields = ('status','attempts','last_error','created_at','sent_at')

class MessageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageLog
        fields = '__all__'

class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = '__all__'
