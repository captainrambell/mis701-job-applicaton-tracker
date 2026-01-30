from django.contrib import admin

from .models import Job, Application, Contact


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "source", "created_at")
    search_fields = ("title", "company", "location", "source")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "status", "applied_date", "next_step_date")
    list_filter = ("status",)
    search_fields = ("job__title", "job__company")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "job", "email", "phone")
    search_fields = ("name", "role", "job__title", "job__company")
