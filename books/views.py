from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from .models import Book, Author, Category
from .utils import get_featured_books, get_recent_books
from accounts.forms import CustomUserCreationForm, ProfileUpdateForm
from accounts.models import CustomUser

def home(request):
    """Homepage view with featured and recent books"""
    context = {
        'featured_books': get_featured_books(limit=8),
        'recent_books': get_recent_books(limit=8),
        'categories': Category.objects.all()[:6],
        'total_books': Book.objects.filter(is_available=True).count(),
        'total_authors': Author.objects.count(),
    }
    return render(request, 'books/home.html', context)

def book_list(request):
    """Book listing page with search and filtering"""
    books = Book.objects.filter(is_available=True).select_related().prefetch_related('authors', 'categories')
    
    context = {
        'books': books[:12],  # First 12 books for now
        'categories': Category.objects.all(),
    }
    
    return render(request, 'books/book_list.html', context)

def book_detail(request, pk):
    """Individual book detail page with comprehensive information"""
    book = get_object_or_404(
        Book.objects.select_related().prefetch_related('authors', 'categories'),
        pk=pk,
        is_available=True
    )
    
    # Get recommendations (books in same categories or by same authors)
    recommendations = Book.objects.filter(
        Q(categories__in=book.categories.all()) |
        Q(authors__in=book.authors.all())
    ).exclude(
        id=book.id
    ).filter(
        is_available=True
    ).distinct().select_related().prefetch_related('authors')[:4]
    
    context = {
        'book': book,
        'recommendations': recommendations,
        'in_stock': book.is_in_stock,
    }
    
    return render(request, 'books/book_detail.html', context)

def category_detail(request, slug):
    """Category page showing all books in a category"""
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(categories=category, is_available=True)
    
    context = {
        'category': category,
        'books': books[:12],  # First 12 books
    }
    
    return render(request, 'books/category_detail.html', context)

def author_detail(request, pk):
    """Author page showing all books by an author"""
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(authors=author, is_available=True)
    
    context = {
        'author': author,
        'books': books[:12],  # First 12 books
    }
    
    return render(request, 'books/author_detail.html', context)

def search_ajax(request):
    """AJAX search for live search functionality"""
    query = request.GET.get('q', '')
    
    if len(query) < 3:
        return JsonResponse({'results': []})
    
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(authors__name__icontains=query)
    ).filter(is_available=True).distinct()[:5]
    
    results = []
    for book in books:
        results.append({
            'id': str(book.id),
            'title': book.title,
            'authors': book.authors_list,
            'price': str(book.price),
            'url': book.get_absolute_url(),
        })
    
    return JsonResponse({'results': results})

def about(request):
    """About Us page"""
    return render(request, 'pages/about.html')

def contact(request):
    """Contact Us page"""
    return render(request, 'pages/contact.html')
