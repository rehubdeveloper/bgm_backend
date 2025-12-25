from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from messaging.models.message_log import MessageLog
from messaging.handlers.dispatch import dispatch_email_and_whatsapp

@extend_schema(
    tags=["Messaging"],
    summary="Resend a failed message",
    description="Admin-only: resend a message identified by MessageLog ID. Resends to the same recipient."
)
class ResendMessageView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, log_id: int):
        try:
            log = MessageLog.objects.get(id=log_id)
        except MessageLog.DoesNotExist:
            return Response({"error": "Log not found"}, status=status.HTTP_404_NOT_FOUND)

        # Determine channel
        if log.channel == "email":
            emails = [log.recipient]
            result = dispatch_email_and_whatsapp(subject=log.subject, html_body=log.html_body, plaintext=log.body, email_recipients=emails, whatsapp_recipients=[])
        else:
            result = dispatch_email_and_whatsapp(subject=log.subject, html_body=log.html_body, plaintext=log.body, email_recipients=[], whatsapp_recipients=[log.recipient])

        # Create new log entry will be recorded by dispatch
        return Response({"status": "resent", "result": result})
