from django.contrib import admin
from django.utils.html import format_html

from restaurant_site.admin import admin_site

from .models import ContactMessage


@admin.register(ContactMessage, site=admin_site)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'status_badge', 'submitted_at')
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('name', 'contact_info', 'message')
    ordering = ('is_read', '-submitted_at')
    actions = ('mark_as_read', 'mark_as_unread')

    def status_badge(self, obj):
        if obj.is_read:
            return "Read"
        return format_html('<strong style="color:#c0392b;">Unread</strong>')
    status_badge.short_description = "Status"
    status_badge.admin_order_field = 'is_read'

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} message(s) marked as read.")

    @admin.action(description="Mark selected messages as unread")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} message(s) marked as unread.")
