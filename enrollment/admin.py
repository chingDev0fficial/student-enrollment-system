from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Admin view for Student

    list_display = ("first_name", "last_name", "email", "date_enrolled")
    list_filter = ("date_enrolled", "school_name_graduated")
    search_fields = ("first_name", "last_name", "email", "school_name_graduated")
    ordering = ("-date_enrolled",)
    readonly_fields = ("date_enrolled", "last_updated")
    fieldsets = (
        (
            "Personal Information",
            {"fields": ("first_name", "middle_name", "last_name", "email", "birthday")},
        ),
        ("Address Information", {"fields": ("address",)}),
        ("Academic Information", {"fields": ("school_name_graduated",)}),
        (
            "Parent Information",
            {
                "fields": (
                    "parent_full_name",
                    "relationship",
                    "parent_phone",
                    "parent_email",
                    "parent_occupation",
                    "parent_workplace",
                    "parent_address",
                    "alternate_contact",
                )
            },
        ),
        (
            "System Information",
            {"fields": ("date_enrolled", "last_updated"), "classes": ("collapse",)},
        ),
    )
