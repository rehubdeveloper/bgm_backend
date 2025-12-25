from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from messaging.serializers.outbound_serializer import OutboundMessageSerializer
from messaging.models.outbound_message import OutboundMessage
from messaging.handlers.dispatch import dispatch_email_and_whatsapp

@extend_schema(
    tags=["Messaging"],
    summary="Send a custom message (email &/or WhatsApp)",
    description="Admin-only: send immediate messages to provided recipients. This bypasses automatic triggers.",
    request=OutboundMessageSerializer,
    responses={200: OpenApiParameter(name="status", description="Result summary", required=False, type=str)}
)
class SendMessageView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = OutboundMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Save outbound record (pending)
        outbound = OutboundMessage.objects.create(
            channel=data.get("channel", "email"),
            subject=data.get("subject"),
            body=data.get("body"),
            html_body=data.get("html_body"),
            recipients=data.get("recipients", []),
            related_type=data.get("related_type"),
            related_id=data.get("related_id"),
            status="pending"
        )

        # Dispatch synchronously (or you can push to Celery here)
        email_recipients = [r for r in outbound.recipients if "@" in r]
        whatsapp_recipients = [r for r in outbound.recipients if "@" not in r]

        result = dispatch_email_and_whatsapp(
            subject=outbound.subject or "",
            html_body=outbound.html_body,
            plaintext=outbound.body,
            email_recipients=email_recipients,
            whatsapp_recipients=whatsapp_recipients,
            related_type=outbound.related_type,
            related_id=outbound.related_id
        )

        outbound.attempts += 1
        if (result.get("email") and result["email"]["success"]) or (result.get("whatsapp") and result["whatsapp"]["success"]):
            outbound.status = "sent"
            outbound.sent_at = outbound.sent_at or None
        else:
            outbound.status = "failed"
            outbound.last_error = str(result)
        outbound.save()
        return Response({"status": "dispatched", "result": result}, status=status.HTTP_200_OK)
