from django.db.models.signals import post_save
from django.dispatch import receiver
from contents.models.testimony import Testimony
from messaging.handlers.dispatch import dispatch_email_and_whatsapp
from django.template.loader import render_to_string
from django.conf import settings  # to get FRONTEND_URL


@receiver(post_save, sender=Testimony)
def notify_member_on_status_change(sender, instance: Testimony, created, **kwargs):
    """
    Notify member when their testimony is approved or rejected.
    Only act on updates, not creation.
    """
    if created:
        return  # skip new testimonies

    if not instance.member:
        return

    # Build testimony link
    frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
    testimony_link = f"{frontend_url}/testimonies/{instance.id}"

    # Approved
    if instance.status == "approved":
        context = {
            "member_name": instance.member.first_name,
            "text": instance.text,
            "link": testimony_link,
        }
        html_message = render_to_string("messaging/testimony_approved.html", context)
        plaintext_message = f"Hi {instance.member.first_name}, your testimony has been approved.\nView it here: {testimony_link}"

        dispatch_email_and_whatsapp(
            subject="Your testimony was approved",
            html_body=html_message,
            plaintext=plaintext_message,
            email_recipients=[instance.member.email] if instance.member.email else [],
            whatsapp_recipients=[instance.member.phone] if instance.member.phone else [],
            related_type="testimony",
            related_id=instance.id
        )

    # Rejected
    elif instance.status == "rejected":
        reason = getattr(instance, "rejection_reason", "No reason provided")
        context = {
            "member_name": instance.member.first_name,
            "text": instance.text,
            "reason": reason,
            "link": testimony_link,
        }
        html_message = render_to_string("messaging/testimony_rejected.html", context)
        plaintext_message = f"Hi {instance.member.first_name}, your testimony was rejected. Reason: {reason}\nView it here: {testimony_link}"

        dispatch_email_and_whatsapp(
            subject="Your testimony was rejected",
            html_body=html_message,
            plaintext=plaintext_message,
            email_recipients=[instance.member.email] if instance.member.email else [],
            whatsapp_recipients=[instance.member.phone] if instance.member.phone else [],
            related_type="testimony",
            related_id=instance.id
        )
