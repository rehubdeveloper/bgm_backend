from rest_framework import serializers
from messaging.models.template import MessageTemplate

class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = "__all__"
