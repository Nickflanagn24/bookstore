from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Order, OrderItem, OrderStatusHistory

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('book_title', 'book_authors', 'unit_price', 'total_price')
    fields = ('book', 'book_title', 'book_authors', 'quantity', 'unit_price', 'total_price')
    
    def total_price(self, obj):
        if obj.pk:
            return f"£{obj.total_price:.2f}"
        return ""
    total_price.short_description = "Total"

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('changed_at',)
    fields = ('from_status', 'to_status', 'notes', 'changed_by', 'changed_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'customer_name', 'status_badge', 'total_amount', 
        'total_items', 'payment_status', 'created_at'
    )
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = (
        'order_number', 'customer_email', 'customer_first_name', 
        'customer_last_name', 'stripe_session_id'
    )
    readonly_fields = (
        'id', 'order_number', 'stripe_session_id', 'stripe_payment_intent_id',
        'created_at', 'updated_at', 'total_items'
    )
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'order_number', 'status', 'created_at', 'updated_at', 'confirmed_at')
        }),
        ('Customer Information', {
            'fields': ('user', 'customer_email', 'customer_first_name', 'customer_last_name')
        }),
        ('Payment Information', {
            'fields': ('total_amount', 'payment_status', 'stripe_session_id', 'stripe_payment_intent_id')
        }),
        ('Order Summary', {
            'fields': ('total_items',)
        }),
    )
    
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    
    def customer_name(self, obj):
        return obj.customer_full_name
    customer_name.short_description = "Customer"
    customer_name.admin_order_field = 'customer_first_name'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#17a2b8',
            'processing': '#fd7e14',
            'shipped': '#6f42c1',
            'delivered': '#28a745',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"
    status_badge.admin_order_field = 'status'
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            # Record status change
            old_status = Order.objects.get(pk=obj.pk).status
            OrderStatusHistory.objects.create(
                order=obj,
                from_status=old_status,
                to_status=obj.status,
                changed_by=request.user,
                notes=f"Status changed by {request.user.get_full_name() or request.user.username}"
            )
            
            if obj.status == 'confirmed' and not obj.confirmed_at:
                obj.confirmed_at = timezone.now()
        
        super().save_model(request, obj, form, change)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_link', 'book_title', 'quantity', 'unit_price', 'total_price')
    list_filter = ('created_at',)
    search_fields = ('book_title', 'order__order_number')
    readonly_fields = ('total_price',)
    
    def order_link(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
    order_link.short_description = "Order"
    order_link.admin_order_field = 'order__order_number'

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order_link', 'from_status', 'to_status', 'changed_by', 'changed_at')
    list_filter = ('to_status', 'changed_at')
    search_fields = ('order__order_number', 'notes')
    readonly_fields = ('changed_at',)
    
    def order_link(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
    order_link.short_description = "Order"
    order_link.admin_order_field = 'order__order_number'
