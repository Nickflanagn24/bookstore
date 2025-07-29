"""
Shopping cart models for the Tales & Tails application.

This module defines models for shopping cart functionality, including the
cart itself and individual cart items. It provides methods for calculating
totals and managing item quantities.
"""
import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models

from books.models import Book


class Cart(models.Model):
    """
    Shopping cart model for Tales & Tails.
    
    Represents a user's shopping cart, containing items they intend to purchase.
    Each user has a single cart associated with their account, and the cart
    contains multiple cart items.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Cart model."""
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"
        ordering = ['-updated_at']

    def __str__(self):
        """Return string representation of the cart."""
        return f"Cart for {self.user.full_name}"

    @property
    def total_items(self):
        """
        Get total number of items in cart.
        
        Returns:
            int: Sum of quantities of all items in the cart
        """
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        """
        Calculate total price of all items in cart.
        
        Returns:
            Decimal: Total price of all items in the cart
        """
        return sum(item.total_price for item in self.items.all())

    @property
    def is_empty(self):
        """
        Check if cart is empty.
        
        Returns:
            bool: True if cart has no items, False otherwise
        """
        return self.items.count() == 0


class CartItem(models.Model):
    """
    Individual items in the shopping cart.
    
    Represents a specific book in a user's cart, along with the quantity
    and calculated total price. Ensures quantities don't exceed available stock.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the CartItem model."""
        unique_together = ('cart', 'book')
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ['-added_at']

    def __str__(self):
        """Return string representation of the cart item."""
        return f"{self.quantity}x {self.book.title}"

    @property
    def total_price(self):
        """
        Calculate total price for this cart item.
        
        Returns:
            Decimal: Product of book price and quantity
        """
        return Decimal(str(self.book.price)) * self.quantity

    def save(self, *args, **kwargs):
        """
        Save cart item after ensuring quantity doesn't exceed stock.
        
        Limits the quantity to the available stock quantity of the book
        before saving the cart item to the database.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        if self.quantity > self.book.stock_quantity:
            self.quantity = self.book.stock_quantity
        super().save(*args, **kwargs)
        