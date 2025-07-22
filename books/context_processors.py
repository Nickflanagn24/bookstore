from books.models import Book, Author, Category

def site_stats(request):
    """Provide dynamic site statistics for templates"""
    return {
        'total_books': Book.objects.count(),
        'total_authors': Author.objects.count(), 
        'total_categories': Category.objects.count(),
        'available_books': Book.objects.filter(is_available=True).count(),
        'featured_books': Book.objects.filter(is_featured=True).count(),
    }
