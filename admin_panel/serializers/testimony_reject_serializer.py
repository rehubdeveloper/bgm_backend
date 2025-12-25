# admin_panel/serializers/testimony_reject_serializer.py
from rest_framework import serializers

class RejectTestimonySerializer(serializers.Serializer):
    rejection_reason = serializers.CharField(
        required=True, 
        max_length=1000, 
        help_text="Provide a reason for rejecting the testimony"
    )
