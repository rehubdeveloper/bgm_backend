from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from members.models.member import Member

@admin.register(Member)
class MemberAdmin(UserAdmin):
    model = Member
    list_display = (
        "email", "first_name", "last_name", "phone",
        "department", "is_active", "is_staff", "is_superuser", "created_at"
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "marital_status", "gender", "department")
    search_fields = ("email", "first_name", "last_name", "phone")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone", "department", "date_of_birth", "marital_status", "gender", "occupation", "address")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2", "is_active", "is_staff"),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")
