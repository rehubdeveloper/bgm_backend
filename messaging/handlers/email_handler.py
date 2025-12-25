import traceback
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email(subject: str, html_body: str, plaintext: str, recipients: list, from_email=None):
    """
    Synchronous email send. Returns (success: bool, error: str|None).
    """
    if not from_email:
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)

    try:
        # If plaintext not provided, create a simple fallback
        if not plaintext:
            plaintext = "You have a new message from Believers Glorious Ministry."

        # Create message
        msg = EmailMultiAlternatives(subject=subject, body=plaintext, from_email=from_email, to=recipients)
        if html_body:
            msg.attach_alternative(html_body, "text/html")
        msg.send()
        return True, None
    except Exception as exc:
        tb = traceback.format_exc()
        return False, f"{str(exc)}\n{tb}"
