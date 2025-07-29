"""
Database models for the orders application.

This module defines the data models for order management, including orders,
order items, and order status history tracking.
"""
import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse

from books.models import Book


class Order(models.Model):
    """
    Order model for tracking customer purchases.
    
    Stores comprehensive order information including customer details,
    payment information, and order status. Maintains a snapshot of
    customer information at the time of purchase.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Order identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # Customer information
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    
    # Order details
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment information
    stripe_session_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    payment_status = models.CharField(max_length=20, default='pending')
    
    # Customer details (snapshot at time of order)
    customer_email = models.EmailField()
    customer_first_name = models.CharField(max_length=100)
    customer_last_name = models.CharField(max_length=100)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        """Meta options for the Order model."""
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['stripe_session_id']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        """Return a string representation of the order."""
        return f"Order {self.order_number} - {self.user.full_name}"
    
    def save(self, *args, **kwargs):
        """
        Save the order after generating an order number if needed.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """
        Generate a unique order number.
        
        Creates a unique order number in the format TT-YYYYMMDD-XXXXX
        where TT stands for Tales & Tails, followed by the date and
        a random alphanumeric string.
        
        Returns:
            str: The generated order number
        """
        import random
        import string
        from django.utils import timezone
        
        # Format: TT-YYYYMMDD-XXXXX (TT = Tales & Tails)
        date_str = timezone.now().strftime('%Y%m%d')
        random_str = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=5)
        )
        return f"TT-{date_str}-{random_str}"
    
    @property
    def customer_full_name(self):
        """
        Get the customer's full name.
        
        Returns:
            str: The customer's first and last name combined
        """
        return f"{self.customer_first_name} {self.customer_last_name}"
    
    @property
    def total_items(self):
        """
        Get the total number of items in the order.
        
        Returns:
            int: Sum of all item quantities in the order
        """
        return sum(item.quantity for item in self.items.all())
    
    def get_absolute_url(self):
        """
        Get the URL for the order detail page.
        
        Returns:
            str: URL path to the order detail view
        """
        return reverse(
            'orders:order_detail',
            kwargs={'order_number': self.order_number}
        )

    @property
    def total_price(self):
        """
        Calculate total price of all items in the order.
        
        Returns:
            Decimal: Sum of all item prices multiplied by their quantities
        """
        return sum(
            (item.unit_price or 0) * (item.quantity or 0) 
            for item in self.items.all()
        )


class OrderItem(models.Model):
    """
    Individual items within an order.
    
    Represents a specific book in an order, including quantity and pricing.
    Stores a snapshot of book details at the time of purchase.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    # Item details (snapshot at time of order)
    book_title = models.CharField(max_length=300)
    book_authors = models.CharField(max_length=500)
    book_isbn = models.CharField(max_length=20, blank=True)
    
    # Pricing and quantity
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Meta options for the OrderItem model."""
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        unique_together = ('order', 'book')
    
    def __str__(self):
        """Return a string representation of the order item."""
        return f"{self.quantity}x {self.book_title} (Order: {self.order.order_number})"
    
    @property
    def total_price(self):
        """
        Calculate total price for this item.
        
        Returns:
            Decimal: Product of unit price and quantity
        """
        return (self.unit_price or 0) * (self.quantity or 0)
    
    def save(self, *args, **kwargs):
        """
        Save the order item after ensuring book details are captured.
        
        Takes a snapshot of the book details at the time of order creation
        if they aren't already set.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        # Snapshot book details at time of order
        if not self.book_title and self.book:
            self.book_title = self.book.title
            self.book_authors = self.book.authors_list
            self.book_isbn = self.book.isbn_13 or self.book.isbn_10 or ''
            self.unit_price = self.book.price
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    """
    Track order status changes.
    
    Records the history of status changes for orders, including who made
    the change, when it occurred, and any additional notes.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        related_name='status_history',
        on_delete=models.CASCADE
    )
    
    from_status = models.CharField(max_length=20, blank=True)
    to_status = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Meta options for the OrderStatusHistory model."""
        ordering = ['-changed_at']
        verbose_name = "Order Status History"
        verbose_name_plural = "Order Status Histories"
    
    def __str__(self):
        """Return a string representation of the status change."""
        return f"Order {self.order.order_number}: {self.from_status} → {self.to_status}"
        