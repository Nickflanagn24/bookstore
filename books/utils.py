"""
Utility functions for the Books application.

This module provides helper functions for book-related operations such as
searching, retrieving featured books, syncing with Google Books API,
and generating book recommendations.
"""

from typing import List, Dict, Optional
from .models import Book, Author, Category
from .services import google_books_api
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search_books_local(query: str, page: int = 1, per_page: int = 12) -> Dict:
    """
    Search for books in the local database.
    
    Performs a search across multiple book fields including title, author,
    description, and category. Results are paginated for display.
    
    Args:
        query: Search query string
        page: Page number for pagination
        per_page: Number of books per page
        
    Returns:
        Dictionary with search results and pagination information
    """
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(authors__name__icontains=query) |
        Q(description__icontains=query) |
        Q(categories__name__icontains=query)
    ).distinct().select_related().prefetch_related('authors', 'categories')
    
    paginator = Paginator(books, per_page)
    
    try:
        books_page = paginator.page(page)
    except PageNotAnInteger:
        books_page = paginator.page(1)
    except EmptyPage:
        books_page = paginator.page(paginator.num_pages)
    
    return {
        'books': books_page,
        'has_results': books.exists(),
        'total_count': paginator.count,
        'page_range': paginator.get_elided_page_range(books_page.number),
    }


def get_featured_books(limit: int = 8) -> List[Book]:
    """
    Get featured books for homepage display.
    
    Retrieves books marked as featured and available for purchase,
    optimised with related object prefetching.
    
    Args:
        limit: Maximum number of books to return
        
    Returns:
        List of featured Book objects
    """
    return Book.objects.filter(
        is_featured=True, 
        is_available=True
    ).select_related().prefetch_related('authors')[:limit]


def get_recent_books(limit: int = 8) -> List[Book]:
    """
    Get recently added books.
    
    Retrieves the most recently added books that are available for purchase,
    ordered by creation date and optimised with related object prefetching.
    
    Args:
        limit: Maximum number of books to return
        
    Returns:
        List of recently added Book objects
    """
    return Book.objects.filter(
        is_available=True
    ).select_related().prefetch_related('authors').order_by('-created_at')[:limit]


def get_books_by_category(category_slug: str, page: int = 1, per_page: int = 12) -> Dict:
    """
    Get books by category with pagination.
    
    Retrieves books belonging to a specific category and paginates the results.
    
    Args:
        category_slug: URL slug of the category
        page: Page number for pagination
        per_page: Number of books per page
        
    Returns:
        Dictionary containing category, books, and pagination information
    """
    try:
        category = Category.objects.get(slug=category_slug)
        books = Book.objects.filter(
            categories=category, 
            is_available=True
        ).select_related().prefetch_related('authors', 'categories')
        
        paginator = Paginator(books, per_page)
        
        try:
            books_page = paginator.page(page)
        except PageNotAnInteger:
            books_page = paginator.page(1)
        except EmptyPage:
            books_page = paginator.page(paginator.num_pages)
        
        return {
            'category': category,
            'books': books_page,
            'total_count': paginator.count,
            'page_range': paginator.get_elided_page_range(books_page.number),
        }
    except Category.DoesNotExist:
        return {
            'category': None,
            'books': None,
            'total_count': 0,
            'page_range': [],
        }


def sync_book_from_google(google_books_id: str) -> Optional[Book]:
    """
    Synchronise a single book from Google Books API.
    
    Retrieves book data from the Google Books API and creates or updates
    the corresponding book record in the local database, including
    associated authors and categories.
    
    Args:
        google_books_id: Google Books volume ID
        
    Returns:
        Book instance if successful, None otherwise
    """
    book_data = google_books_api.get_book_by_id(google_books_id)
    
    if not book_data:
        return None
    
    extracted_data = google_books_api.extract_book_data(book_data)
    
    # Check if book already exists
    book, created = Book.objects.get_or_create(
        google_books_id=extracted_data['google_books_id'],
        defaults={
            'title': extracted_data['title'],
            'subtitle': extracted_data['subtitle'],
            'description': extracted_data['description'],
            'price': 19.99,  # Default price
            'stock_quantity': 10,
            'is_available': True,
        }
    )
    
    if created:
        # Add authors
        for author_name in extracted_data['authors']:
            author, _ = Author.objects.get_or_create(name=author_name)
            book.authors.add(author)
        
        # Add categories
        for category_name in extracted_data['categories']:
            from django.utils.text import slugify
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': slugify(category_name)}
            )
            book.categories.add(category)
    
    return book


def get_book_recommendations(book: Book, limit: int = 4) -> List[Book]:
    """
    Get book recommendations based on categories and authors.
    
    Generates personalised book recommendations by finding books that share
    categories or authors with the specified book, excluding the original book.
    
    Args:
        book: Book instance to base recommendations on
        limit: Maximum number of recommendations to return
        
    Returns:
        List of recommended Book objects
    """
    # Get books in same categories or by same authors
    recommendations = Book.objects.filter(
        Q(categories__in=book.categories.all()) |
        Q(authors__in=book.authors.all())
    ).exclude(
        id=book.id
    ).filter(
        is_available=True
    ).distinct().select_related().prefetch_related('authors')[:limit]
    
    return list(recommendations)
    