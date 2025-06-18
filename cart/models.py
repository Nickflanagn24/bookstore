from django.db import models
from django.conf import settings
from books.models import Book
import uuid
from decimal import Decimal

class Cart(models.Model):
    """Elegant shopping cart model for Tales & Tails"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"
        ordering = ['-updated_at']

    def __str__(self):
        return f"Cart for {self.user.full_name}"

    @property
    def total_items(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        """Calculate total price of all items in cart"""
        return sum(item.total_price for item in self.items.all())

    @property
    def is_empty(self):
        """Check if cart is empty"""
        return self.items.count() == 0


class CartItem(models.Model):
    """Individual items in the shopping cart"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'book')
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.quantity}x {self.book.title}"

    @property
    def total_price(self):
        """Calculate total price for this cart item"""
        return Decimal(str(self.book.price)) * self.quantity

    def save(self, *args, **kwargs):
        """Ensure quantity doesn't exceed stock"""
        if self.quantity > self.book.stock_quantity:
            self.quantity = self.book.stock_quantity
        super().save(*args, **kwargs)