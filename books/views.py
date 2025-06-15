from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from .models import Book, Author, Category
from .utils import get_featured_books, get_recent_books

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
    """Individual book detail page"""
    book = get_object_or_404(Book, pk=pk, is_available=True)
    
    context = {
        'book': book,
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
