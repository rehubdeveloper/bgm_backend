from django.contrib import admin
from contents.models.about import About
from contents.models.devotional import DailyDevotional
from contents.models.event import Event
from contents.models.sermon import Sermon
from contents.models.testimony import Testimony


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "title", "updated_at")
    list_filter = ("type",)
    search_fields = ("title", "content")
    ordering = ("-updated_at",)  # was using 'created_at' before


@admin.register(DailyDevotional)
class DailyDevotionalAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "bible_verse", "created_at")
    search_fields = ("title", "bible_verse")
    ordering = ("-created_at",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "event_date", "created_at")
    search_fields = ("title", "description")
    ordering = ("-event_date",)


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "preacher", "created_at")
    search_fields = ("title", "preacher")
    ordering = ("-created_at",)


@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ("id", "member_name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("text",)
    ordering = ("-created_at",)

    def member_name(self, obj):
        return f"{obj.member.first_name} {obj.member.last_name}" if obj.member else "Anonymous"
    member_name.short_description = "Member"
