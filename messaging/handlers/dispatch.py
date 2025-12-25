from messaging.handlers.email_handler import send_email
from messaging.handlers.whatsapp_handler import send_whatsapp_message
from messaging.models.message_log import MessageLog

def dispatch_email_and_whatsapp(subject, html_body, plaintext, email_recipients, whatsapp_recipients, related_type=None, related_id=None):
    """
    Try send email and whatsapp synchronously and create logs.
    Returns dict with results.
    """
    results = {"email": None, "whatsapp": None}

    if email_recipients:
        success, error = send_email(subject=subject, html_body=html_body, plaintext=plaintext, recipients=email_recipients)
        # Log each recipient
        for r in email_recipients:
            MessageLog.objects.create(
                channel="email",
                subject=subject,
                body=plaintext,
                html_body=html_body,
                recipient=r,
                related_type=related_type,
                related_id=related_id,
                status="sent" if success else "failed",
                error=error
            )
        results["email"] = {"success": success, "error": error}

    if whatsapp_recipients:
        success, error = send_whatsapp_message(whatsapp_recipients, plaintext or html_body or subject)
        for r in whatsapp_recipients:
            MessageLog.objects.create(
                channel="whatsapp",
                subject=subject,
                body=plaintext,
                html_body=html_body,
                recipient=r,
                related_type=related_type,
                related_id=related_id,
                status="sent" if success else "failed",
                error=error
            )
        results["whatsapp"] = {"success": success, "error": error}

    return results
