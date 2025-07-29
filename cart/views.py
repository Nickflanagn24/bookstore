"""
View functions for the cart application.

This module provides Django view functions for managing the shopping cart,
including adding, updating, removing, and displaying cart items.
"""
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from books.models import Book
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    """
    Display the user's shopping cart.
    
    Retrieves or creates a cart for the authenticated user and
    shows all items within it, along with totals.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered cart detail template with cart context
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('book').all(),
        'total_items': cart.total_items,
        'total_price': cart.total_price,
    }
    return render(request, 'cart/cart_detail.html', context)


@login_required
@require_POST
def add_to_cart(request, book_id):
    """
    Add a book to the user's shopping cart.
    
    Adds the specified book to the user's cart or increases the quantity
    if already present. Handles stock validation and provides feedback.
    Supports both standard and AJAX requests.
    
    Args:
        request: The HTTP request object
        book_id: UUID of the book to add
        
    Returns:
        Redirect to book detail page or JSON response for AJAX requests
    """
    book = get_object_or_404(Book, id=book_id, is_available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if book is in stock
    if not book.is_in_stock:
        messages.error(
            request,
            f"Sorry, '{book.title}' is currently out of stock."
        )
        return redirect('books:book_detail', pk=book_id)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': 1}
    )
    
    if not created:
        # Item already in cart, increase quantity
        if cart_item.quantity < book.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(
                request,
                f"Added another '{book.title}' to your cart."
            )
        else:
            messages.warning(
                request,
                f"Cannot add more '{book.title}' - maximum stock reached."
            )
    else:
        messages.success(request, f"'{book.title}' added to your cart!")
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'message': f"'{book.title}' added to cart!"
        })
    
    return redirect('books:book_detail', pk=book_id)


@login_required
@require_POST
def update_cart_item(request, item_id):
    """
    Update the quantity of an item in the cart.
    
    Changes the quantity of a cart item, removes it if quantity is zero,
    and validates against available stock. Provides user feedback.
    
    Args:
        request: The HTTP request object
        item_id: UUID of the cart item to update
        
    Returns:
        Redirect to cart detail page
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(
                request,
                f"'{cart_item.book.title}' removed from cart."
            )
        elif quantity <= cart_item.book.stock_quantity:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(
                request,
                f"Updated '{cart_item.book.title}' quantity."
            )
        else:
            messages.error(
                request,
                f"Cannot add {quantity} items - only "
                f"{cart_item.book.stock_quantity} in stock."
            )
            
    except ValueError:
        messages.error(request, "Invalid quantity specified.")
    
    return redirect('cart:cart_detail')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """
    Remove an item from the cart.
    
    Deletes the specified item from the user's cart and provides feedback.
    Supports both standard and AJAX requests.
    
    Args:
        request: The HTTP request object
        item_id: UUID of the cart item to remove
        
    Returns:
        Redirect to cart detail page or JSON response for AJAX requests
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    book_title = cart_item.book.title
    cart_item.delete()
    
    messages.success(request, f"'{book_title}' removed from your cart.")
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'message': f"'{book_title}' removed from cart."
        })
    
    return redirect('cart:cart_detail')


@login_required
def clear_cart(request):
    """
    Clear all items from the user's cart.
    
    Removes all items from the user's shopping cart and provides feedback.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Redirect to cart detail page
    """
    try:
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        messages.success(request, "Your cart has been cleared.")
    except Cart.DoesNotExist:
        pass
    
    return redirect('cart:cart_detail')
    