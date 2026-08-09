from django.template.loader import render_to_string
from django.conf import settings
from .models import MessageLog

def send_email(subject, html_body, plaintext, recipients):
    from django.core.mail import EmailMultiAlternatives, get_connection
    try:
        msg = EmailMultiAlternatives(subject=subject, body=plaintext or subject, to=recipients, from_email=getattr(settings,'DEFAULT_FROM_EMAIL',None))
        if html_body:
            msg.attach_alternative(html_body, 'text/html')
        msg.send()
        for r in recipients:
            MessageLog.objects.create(channel='email', subject=subject, body=plaintext, html_body=html_body, recipient=r, status='sent')
        return True, None
    except Exception as exc:
        return False, str(exc)

def send_whatsapp(recipients, message):
    for r in recipients:
        MessageLog.objects.create(channel='whatsapp', body=message, recipient=r, status='sent')
    return True, None
