from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','email','phone','department','is_active','created_at')
