from django.db import models
from django.conf import settings
from books.models import Book
import uuid
from decimal import Decimal

class Order(models.Model):
    """Order model for tracking customer purchases"""
    
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    
    # Order details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment information
    stripe_session_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
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
        return f"Order {self.order_number} - {self.user.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Generate unique order number"""
        import random
        import string
        from django.utils import timezone
        
        # Format: TT-YYYYMMDD-XXXXX (TT = Tales & Tails)
        date_str = timezone.now().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"TT-{date_str}-{random_str}"
    
    @property
    def customer_full_name(self):
        return f"{self.customer_first_name} {self.customer_last_name}"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('orders:order_detail', kwargs={'order_number': self.order_number})

    @property
    def total_price(self):
        """Calculate total price of all items in the order"""
        return sum((item.unit_price or 0) * (item.quantity or 0) for item in self.items.all())


class OrderItem(models.Model):
    """Individual items within an order"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    # Item details (snapshot at time of order)
    book_title = models.CharField(max_length=300)
    book_authors = models.CharField(max_length=500)
    book_isbn = models.CharField(max_length=20, blank=True)
    
    # Pricing and quantity
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_price(self):
        """Calculate total price of item"""
        return (self.unit_price or 0) * (self.quantity or 0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        unique_together = ('order', 'book')
    
    def __str__(self):
        return f"{self.quantity}x {self.book_title} (Order: {self.order.order_number})"
    
    @property
    def total_price(self):
        return (self.unit_price or 0) * (self.quantity or 0)
    
    def save(self, *args, **kwargs):
        # Snapshot book details at time of order
        if not self.book_title and self.book:
            self.book_title = self.book.title
            self.book_authors = self.book.authors_list
            self.book_isbn = self.book.isbn_13 or self.book.isbn_10 or ''
            self.unit_price = self.book.price
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    """Track order status changes"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='status_history', on_delete=models.CASCADE)
    
    from_status = models.CharField(max_length=20, blank=True)
    to_status = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name = "Order Status History"
        verbose_name_plural = "Order Status Histories"
    
    def __str__(self):
        return f"Order {self.order.order_number}: {self.from_status} → {self.to_status}"

    @property
    def total_price(self):
        """Calculate total price of all items in the order"""
        return sum((item.unit_price or 0) * (item.quantity or 0) for item in self.items.all())
