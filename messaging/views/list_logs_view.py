from rest_framework import generics, permissions
from messaging.models.message_log import MessageLog
from messaging.serializers.log_serializer import MessageLogSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=["Messaging"],
    summary="List message logs",
    description="List past message send attempts."
)
class MessageLogListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = MessageLog.objects.all().order_by("-created_at")
    serializer_class = MessageLogSerializer
