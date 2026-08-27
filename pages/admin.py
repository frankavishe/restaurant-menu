from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'contact_info', 'message')
