from django.contrib import admin
from django.utils.html import format_html
from .models import NewsletterSubscriber

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'status_badge', 'subscribed_at', 'confirmed_at', 'is_active']
    list_filter = ['is_confirmed', 'is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['confirmation_token', 'subscribed_at', 'confirmed_at']
    
    def status_badge(self, obj):
        if obj.is_confirmed and obj.is_active:
            return format_html('<span style="color: green;">✅ Active</span>')
        elif obj.is_confirmed and not obj.is_active:
            return format_html('<span style="color: orange;">⏸️ Unsubscribed</span>')
        else:
            return format_html('<span style="color: red;">⏳ Pending</span>')
    status_badge.short_description = 'Status'
