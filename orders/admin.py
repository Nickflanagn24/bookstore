"""
Admin configuration for the orders application.

This module defines Django admin interfaces for managing orders and order items,
including custom admin views, inlines, and optimised querysets.
"""
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for OrderItem model.
    
    Provides an inline view of order items within the order admin page,
    with appropriate field display and permissions.
    """
    model = OrderItem
    fields = ['book', 'book_title', 'unit_price', 'quantity', 'total_price']
    readonly_fields = ['book_title', 'total_price']
    extra = 0
    
    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of order items through inline.
        
        Args:
            request: The HTTP request object
            obj: The parent object being edited
            
        Returns:
            bool: Always False to prevent deletion
        """
        # Prevent deletion of order items through inline
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Order model.
    
    Provides a comprehensive interface for managing orders, including
    list display, filtering, search capabilities, and field organisation.
    Includes order items as inline elements.
    """
    list_display = [
        'order_number', 'user', 'status', 'payment_status',
        'total_amount', 'created_at', 'confirmed_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = [
        'order_number', 'user__username', 'user__email', 'customer_email'
    ]
    readonly_fields = [
        'order_number', 'created_at', 'updated_at', 'confirmed_at', 'total_price'
    ]
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_amount', 'total_price')
        }),
        ('Customer Information', {
            'fields': ('customer_email', 'customer_first_name', 'customer_last_name')
        }),
        ('Payment Information', {
            'fields': (
                'payment_status', 'stripe_session_id', 'stripe_payment_intent_id'
            )
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'confirmed_at')
        }),
    )
    
    def get_queryset(self, request):
        """
        Optimise the queryset for the admin list view.
        
        Uses select_related and prefetch_related to reduce database queries
        when displaying orders in the admin interface.
        
        Args:
            request: The HTTP request object
            
        Returns:
            QuerySet: Optimised order queryset
        """
        return (
            super().get_queryset(request)
            .select_related('user')
            .prefetch_related('items', 'items__book')
        )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the OrderItem model.
    
    Provides an interface for managing individual order items with
    appropriate list display, filtering, and search capabilities.
    """
    list_display = ['order', 'book_title', 'unit_price', 'quantity', 'total_price']
    list_filter = ['order__status', 'order__payment_status']
    search_fields = ['order__order_number', 'book_title']
    readonly_fields = ['total_price', 'book_title']
    
    def get_queryset(self, request):
        """
        Optimise the queryset for the admin list view.
        
        Uses select_related to reduce database queries when displaying
        order items in the admin interface.
        
        Args:
            request: The HTTP request object
            
        Returns:
            QuerySet: Optimised order item queryset
        """
        return super().get_queryset(request).select_related('order', 'book')
        