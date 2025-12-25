from django.contrib import admin
from messaging.models.outbound_message import OutboundMessage
from messaging.models.message_log import MessageLog
from messaging.models.template import MessageTemplate

@admin.register(OutboundMessage)
class OutboundAdmin(admin.ModelAdmin):
    list_display = ("id", "channel", "subject", "status", "attempts", "created_at")
    search_fields = ("subject", "related_type")
    readonly_fields = ("created_at", "sent_at")

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ("id", "channel", "recipient", "status", "created_at")
    search_fields = ("recipient", "related_type", "error")

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ("key", "subject", "updated_at")
