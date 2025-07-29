"""
Admin configuration for the books application.

This module registers and configures Django admin interfaces for book-related models,
including Authors, Categories, Books, Reviews, and customer communications.
"""
from django.contrib import admin
from .models import Book, Author, Category, ContactMessage, Newsletter, Review


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Author model.
    
    Customises the admin interface for managing author entries,
    including list displays, filtering, search capabilities,
    and field organisation.
    """
    list_display = ['name', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('name', 'biography', 'photo', 'is_featured')
        }),
        ('Google Books Integration', {
            'fields': ('google_books_id',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    
    Provides an interface for managing book categories with automatic
    slug generation from the category name.
    """
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.
    
    Offers a comprehensive interface for managing book entries,
    including detailed fieldsets for different aspects of book data,
    filtering options, and search capabilities.
    """
    list_display = [
        'title', 'authors_list', 'price', 'stock_quantity', 
        'is_available', 'is_featured', 'created_at'
    ]
    list_filter = [
        'is_available', 'is_featured', 'main_category', 
        'language', 'created_at'
    ]
    search_fields = ['title', 'authors__name', 'isbn_13', 'google_books_id']
    filter_horizontal = ['authors', 'categories']
    readonly_fields = ['id', 'created_at', 'updated_at', 'average_rating', 'ratings_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'authors', 'publisher', 'published_date')
        }),
        ('Content', {
            'fields': ('description', 'page_count', 'language', 'categories', 'main_category')
        }),
        ('Identifiers', {
            'fields': ('google_books_id', 'isbn_10', 'isbn_13'),
            'classes': ('collapse',)
        }),
        ('Images', {
            'fields': ('thumbnail', 'cover_image'),
        }),
        ('E-commerce', {
            'fields': ('price', 'stock_quantity', 'is_available', 'is_featured')
        }),
        ('Ratings', {
            'fields': ('average_rating', 'ratings_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def authors_list(self, obj):
        """
        Generate a formatted list of authors for display in the admin.
        
        Args:
            obj: The Book object being displayed
            
        Returns:
            str: Comma-separated list of author names
        """
        return obj.authors_list
    authors_list.short_description = 'Authors'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ContactMessage model.
    
    Provides an interface for managing customer contact messages,
    including read status management and filtering options.
    """
    list_display = ['subject', 'email', 'first_name', 'last_name', 'submitted_at', 'is_read']
    list_filter = ['is_read', 'submitted_at', 'subject']
    search_fields = ['email', 'subject', 'first_name', 'last_name', 'message']
    readonly_fields = ['submitted_at']
    date_hierarchy = 'submitted_at'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """
        Mark selected messages as read.
        
        Args:
            request: The HTTP request object
            queryset: The queryset of selected ContactMessage objects
            
        Returns:
            None
        """
        count = queryset.update(is_read=True)
        self.message_user(request, f'{count} messages marked as read.')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        """
        Mark selected messages as unread.
        
        Args:
            request: The HTTP request object
            queryset: The queryset of selected ContactMessage objects
            
        Returns:
            None
        """
        count = queryset.update(is_read=False)
        self.message_user(request, f'{count} messages marked as unread.')
    mark_as_unread.short_description = "Mark selected messages as unread"


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Newsletter model.
    
    Provides an interface for managing newsletter subscriptions,
    including activation status management and filtering options.
    """
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'source', 'subscribed_at')
    list_filter = ('is_active', 'source', 'subscribed_at')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('subscribed_at',)
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        """
        Activate selected newsletter subscriptions.
        
        Args:
            request: The HTTP request object
            queryset: The queryset of selected Newsletter objects
            
        Returns:
            None
        """
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscriptions activated.')
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        """
        Deactivate selected newsletter subscriptions.
        
        Args:
            request: The HTTP request object
            queryset: The queryset of selected Newsletter objects
            
        Returns:
            None
        """
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscriptions deactivated.')
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Review model.
    
    Provides an interface for managing book reviews with optimised
    query performance through select_related.
    """
    list_display = ['book', 'user', 'rating', 'title', 'created_at']
    list_filter = ['rating', 'created_at', 'book__categories']
    search_fields = ['book__title', 'user__username', 'title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        """
        Override queryset to optimise database queries.
        
        Uses select_related to reduce the number of database queries
        when retrieving related book and user data.
        
        Args:
            request: The HTTP request object
            
        Returns:
            QuerySet: Optimised queryset with related objects
        """
        return super().get_queryset(request).select_related('book', 'user')
        