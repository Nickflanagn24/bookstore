from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .models import Book, Author, Category
from .utils import search_books_local, get_featured_books, get_recent_books, get_books_by_category

def home(request):
    """Homepage view with featured and recent books"""
    context = {
        'featured_books': get_featured_books(limit=8),
        'recent_books': get_recent_books(limit=8),
        'categories': Category.objects.all()[:6],  # Show top 6 categories
        'total_books': Book.objects.filter(is_available=True).count(),
        'total_authors': Author.objects.count(),
    }
    return render(request, 'books/home.html', context)

def book_list(request):
    """Book listing page with search and filtering"""
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'title')
    page = request.GET.get('page', 1)
    
    # Base queryset
    books = Book.objects.filter(is_available=True).select_related().prefetch_related('authors', 'categories')
    
    # Apply search
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(authors__name__icontains=query) |
            Q(description__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()
    
    # Apply category filter
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            books = books.filter(categories=category)
        except Category.DoesNotExist:
            category = None
    else:
        category = None
    
    # Apply sorting
    sort_options = {
        'title': 'title',
        'price_low': 'price',
        'price_high': '-price',
        'newest': '-created_at',
        'rating': '-average_rating',
    }
    
    if sort_by in sort_options:
        books = books.order_by(sort_options[sort_by])
    
    # Pagination
    paginator = Paginator(books, 12)  # 12 books per page
    
    try:
        books_page = paginator.page(page)
    except PageNotAnInteger:
        books_page = paginator.page(1)
    except EmptyPage:
        books_page = paginator.page(paginator.num_pages)
    
    context = {
        'books': books_page,
        'query': query,
        'category': category,
        'sort_by': sort_by,
        'categories': Category.objects.all(),
        'total_results': paginator.count,
        'page_range': paginator.get_elided_page_range(books_page.number),
    }
    
    return render(request, 'books/book_list.html', context)

def book_detail(request, pk):
    """Individual book detail page"""
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
    page = request.GET.get('page', 1)
    
    books = Book.objects.filter(
        categories=category,
        is_available=True
    ).select_related().prefetch_related('authors', 'categories')
    
    paginator = Paginator(books, 12)
    
    try:
        books_page = paginator.page(page)
    except PageNotAnInteger:
        books_page = paginator.page(1)
    except EmptyPage:
        books_page = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'books': books_page,
        'total_books': paginator.count,
        'page_range': paginator.get_elided_page_range(books_page.number),
    }
    
    return render(request, 'books/category_detail.html', context)

def author_detail(request, pk):
    """Author page showing all books by an author"""
    author = get_object_or_404(Author, pk=pk)
    page = request.GET.get('page', 1)
    
    books = Book.objects.filter(
        authors=author,
        is_available=True
    ).select_related().prefetch_related('authors', 'categories')
    
    paginator = Paginator(books, 12)
    
    try:
        books_page = paginator.page(page)
    except PageNotAnInteger:
        books_page = paginator.page(1)
    except EmptyPage:
        books_page = paginator.page(paginator.num_pages)
    
    context = {
        'author': author,
        'books': books_page,
        'total_books': paginator.count,
        'page_range': paginator.get_elided_page_range(books_page.number),
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
    ).filter(
        is_available=True
    ).distinct().select_related().prefetch_related('authors')[:5]
    
    results = []
    for book in books:
        results.append({
            'id': str(book.id),
            'title': book.title,
            'authors': book.authors_list,
            'price': str(book.price),
            'thumbnail': book.thumbnail or '',
            'url': book.get_absolute_url(),
        })
    
    return JsonResponse({'results': results})