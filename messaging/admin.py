from django.contrib import admin
from .models import OutboundMessage, MessageLog, MessageTemplate

admin.site.register(OutboundMessage)
admin.site.register(MessageLog)
admin.site.register(MessageTemplate)
