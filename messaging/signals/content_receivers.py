from django.db.models.signals import post_save
from django.dispatch import receiver
from contents.models.devotional import DailyDevotional
from contents.models.event import Event
from contents.models.sermon import Sermon
from contents.models.testimony import Testimony

from messaging.handlers.dispatch import dispatch_email_and_whatsapp
from members.models.member import Member  # to fetch recipients
from django.template.loader import render_to_string
from django.conf import settings

def _get_member_contacts(department_ids=None):
    """
    Returns two lists: email_recipients, whatsapp_numbers
    department_ids: optional list to filter members by department
    """
    qs = Member.objects.filter(is_active=True)
    if department_ids:
        qs = qs.filter(department_id__in=department_ids)

    emails = list(qs.values_list("email", flat=True))
    phones = list(qs.values_list("phone", flat=True))
    # filter out empty/None
    emails = [e for e in emails if e]
    phones = [p for p in phones if p]
    return emails, phones

#-----------------------------------------------------------------------
#Send notifications to all members when new devotional content is created
#-----------------------------------------------------------------------
@receiver(post_save, sender=DailyDevotional)
def devotional_created(sender, instance: DailyDevotional, created, **kwargs):
    if not created:
        return
    # Prepare email content
    context = {
        "title": instance.title,
        "bible_verse": instance.bible_verse,
        "reflection": instance.reflection,
        "prayer": instance.prayer,
        "application_tip": instance.application_tip,
        "closing_thought": instance.closing_thought,
        "link": f"{getattr(settings, 'FRONTEND_URL', '')}/devotionals/{instance.id}"
    }
    html = render_to_string("messaging/devotional_notification.html", context)
    plaintext = f"{instance.title}\n{instance.bible_verse}\n{instance.reflection}\nRead more: {context['link']}"

    emails, phones = _get_member_contacts()
    dispatch_email_and_whatsapp(
        subject=f"New Daily Devotional: {instance.title}",
        html_body=html,
        plaintext=plaintext,
        email_recipients=emails,
        whatsapp_recipients=phones,
        related_type="devotional",
        related_id=instance.id
    )


#-----------------------------------------------------------------------
#Send notifications to all members when new event content is created
#-----------------------------------------------------------------------
@receiver(post_save, sender=Event)
def event_created(sender, instance: Event, created, **kwargs):
    if not created:
        return
    context = {
        "title": instance.title,
        "description": instance.description,
        "event_date": instance.event_date,
        "link": f"{getattr(settings, 'FRONTEND_URL', '')}/events/{instance.id}",
    }
    html = render_to_string("messaging/event_notification.html", context)
    plaintext = f"{instance.title}\n{instance.description}\nEvent Date: {instance.event_date}\nDetails: {context['link']}"

    emails, phones = _get_member_contacts()
    dispatch_email_and_whatsapp(
        subject=f"New Event: {instance.title}",
        html_body=html,
        plaintext=plaintext,
        email_recipients=emails,
        whatsapp_recipients=phones,
        related_type="event",
        related_id=instance.id
    )


#-----------------------------------------------------------------------
#Send notifications to all members when new sermon content is created
#-----------------------------------------------------------------------
@receiver(post_save, sender=Sermon)
def sermon_created(sender, instance: Sermon, created, **kwargs):
    if not created:
        return
    context = {
        "title": instance.title,
        "preacher": instance.preacher,
        "description": instance.description,
        "link": f"{getattr(settings, 'FRONTEND_URL', '')}/sermons/{instance.id}",
    }
    html = render_to_string("messaging/sermon_notification.html", context)
    plaintext = f"{instance.title} by {instance.preacher}\nListen/Download: {context['link']}"

    emails, phones = _get_member_contacts()
    dispatch_email_and_whatsapp(
        subject=f"New Sermon Available: {instance.title}",
        html_body=html,
        plaintext=plaintext,
        email_recipients=emails,
        whatsapp_recipients=phones,
        related_type="sermon",
        related_id=instance.id
    )
