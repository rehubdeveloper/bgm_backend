from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from members.models.member import Member  # adjust path if needed


@receiver(post_save, sender=Member)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # only on new registration
        subject = "Welcome to Our Church Family!"
        from_email = None  # uses DEFAULT_FROM_EMAIL
        to_email = [instance.email]

        html_content = render_to_string("messaging/welcome_email.html", {
            "user": instance
        })

        msg = EmailMultiAlternatives(subject, "", from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
