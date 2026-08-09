from django.db.models.signals import post_save
from django.dispatch import receiver
from contents.models import DailyDevotional, Event, Sermon
from .handlers import send_email, send_whatsapp
from django.template.loader import render_to_string
from django.conf import settings
from members.models import Member

def _get_member_contacts():
    qs = Member.objects.filter(is_active=True)
    emails = list(qs.values_list('email', flat=True))
    phones = list(qs.values_list('phone', flat=True))
    emails = [e for e in emails if e]
    phones = [p for p in phones if p]
    return emails, phones

@receiver(post_save, sender=DailyDevotional)
def devotional_created(sender, instance, created, **kwargs):
    if not created:
        return
    context = {'title': instance.title, 'bible_verse': instance.bible_verse, 'reflection': instance.reflection, 'link': f"{getattr(settings,'FRONTEND_URL','')}/devotionals/{instance.id}"}
    html = render_to_string('messaging/devotional_notification.html', context)
    plaintext = f"{instance.title}\n{instance.bible_verse}\nRead: {context['link']}"
    emails, phones = _get_member_contacts()
    if emails:
        send_email(subject=f"New Devotional: {instance.title}", html_body=html, plaintext=plaintext, recipients=emails)
    if phones:
        send_whatsapp(phones, plaintext)

@receiver(post_save, sender=Event)
def event_created(sender, instance, created, **kwargs):
    if not created:
        return
    context = {'title': instance.title, 'description': instance.description, 'event_date': instance.event_date, 'link': f"{getattr(settings,'FRONTEND_URL','')}/events/{instance.id}"}
    html = render_to_string('messaging/event_notification.html', context)
    plaintext = f"{instance.title}\n{instance.description}\nDetails: {context['link']}"
    emails, phones = _get_member_contacts()
    if emails:
        send_email(subject=f"New Event: {instance.title}", html_body=html, plaintext=plaintext, recipients=emails)
    if phones:
        send_whatsapp(phones, plaintext)

@receiver(post_save, sender=Sermon)
def sermon_created(sender, instance, created, **kwargs):
    if not created:
        return
    context = {'title': instance.title, 'preacher': instance.preacher, 'link': f"{getattr(settings,'FRONTEND_URL','')}/sermons/{instance.id}"}
    html = render_to_string('messaging/sermon_notification.html', context)
    plaintext = f"{instance.title} by {instance.preacher}\nListen: {context['link']}"
    emails, phones = _get_member_contacts()
    if emails:
        send_email(subject=f"New Sermon: {instance.title}", html_body=html, plaintext=plaintext, recipients=emails)
    if phones:
        send_whatsapp(phones, plaintext)
