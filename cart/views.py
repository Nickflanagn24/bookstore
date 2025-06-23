from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from books.models import Book
from .models import Cart, CartItem
import json

@login_required
def cart_detail(request):
    """Elegant cart detail view"""
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
    """Add book to cart with elegant feedback"""
    book = get_object_or_404(Book, id=book_id, is_available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if book is in stock
    if not book.is_in_stock:
        messages.error(request, f"Sorry, '{book.title}' is currently out of stock.")
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
            messages.success(request, f"Added another '{book.title}' to your cart.")
        else:
            messages.warning(request, f"Cannot add more '{book.title}' - maximum stock reached.")
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
    """Update cart item quantity with elegant validation"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, f"'{cart_item.book.title}' removed from cart.")
        elif quantity <= cart_item.book.stock_quantity:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Updated '{cart_item.book.title}' quantity.")
        else:
            messages.error(request, f"Cannot add {quantity} items - only {cart_item.book.stock_quantity} in stock.")
            
    except ValueError:
        messages.error(request, "Invalid quantity specified.")
    
    return redirect('cart:cart_detail')

@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart with confirmation"""
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
    """Clear entire cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        messages.success(request, "Your cart has been cleared.")
    except Cart.DoesNotExist:
        pass
    
    return redirect('cart:cart_detail')