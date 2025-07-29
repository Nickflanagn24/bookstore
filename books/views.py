"""
View functions for the books application.

This module provides Django view functions for displaying and managing books,
authors, categories, reviews, and handling various user interactions such as
contact submissions and newsletter signups.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
import json

from .models import Book, Author, Category, ContactMessage, Newsletter, Review
from .utils import get_featured_books, get_recent_books
from .forms import BookForm, ReviewForm
from accounts.forms import CustomUserCreationForm, ProfileUpdateForm
from accounts.models import CustomUser


def home(request):
    """
    Display the homepage with featured and recent books.
    
    Shows a curated selection of featured and recently added books,
    along with category navigation and site statistics.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered homepage template with context data
    """
    context = {
        'featured_books': get_featured_books(limit=8),
        'recent_books': get_recent_books(limit=8),
        'categories': Category.objects.all()[:6],
        'total_books': Book.objects.filter(is_available=True).count(),
        'total_authors': Author.objects.count(),
    }
    return render(request, 'books/home.html', context)


def book_list(request):
    """
    Display the book listing page with search and filtering capabilities.
    
    Shows all available books with pagination, and allows filtering by
    search query terms that match title, author, or ISBN.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered book list template with context data
    """
    books_queryset = Book.objects.filter(
        is_available=True
    ).select_related().prefetch_related('authors', 'categories')
    
    # Handle search query
    query = request.GET.get("q")
    if query:
        books_queryset = books_queryset.filter(
            Q(title__icontains=query) |
            Q(authors__name__icontains=query) |
            Q(isbn__icontains=query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(books_queryset, 12)  # Show 12 books per page
    page = request.GET.get('page')
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    
    context = {
        'books': books,
        'categories': Category.objects.all(),
    }
    
    return render(request, 'books/book_list.html', context)


def book_detail(request, pk):
    """
    Display detailed information for a specific book.
    
    Shows comprehensive information about a book including description,
    authors, categories, and similar book recommendations. Also displays
    review information and review capabilities for authenticated users.
    
    Args:
        request: The HTTP request object
        pk: The UUID primary key of the book
        
    Returns:
        Rendered book detail template with context data
    """
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
    
    # Check if user can review and get user review
    user_can_review = False
    user_review = None
    if request.user.is_authenticated:
        user_can_review = book.user_can_review(request.user)
        user_review = book.get_user_review(request.user)
    
    context = {
        "book": book,
        "recommendations": recommendations,
        "in_stock": book.is_in_stock,
        "user_can_review": user_can_review,
        "user_review": user_review,
    }
    
    return render(request, 'books/book_detail.html', context)


def category_detail(request, slug):
    """
    Display all books belonging to a specific category.
    
    Shows a paginated list of books that belong to the specified category.
    
    Args:
        request: The HTTP request object
        slug: The URL slug of the category
        
    Returns:
        Rendered category detail template with context data
    """
    category = get_object_or_404(Category, slug=slug)
    
    # Get all books in this category
    books_list = Book.objects.filter(
        categories=category, 
        is_available=True
    ).order_by("-created_at")
    
    # Add pagination (12 books per page to match books page)
    paginator = Paginator(books_list, 12)
    page_number = request.GET.get("page")
    books = paginator.get_page(page_number)
    
    context = {
        "category": category,
        "books": books,
    }
    
    return render(request, "books/category_detail.html", context)


def author_detail(request, pk):
    """
    Display an author's profile and books.
    
    Shows information about an author and a paginated list of their books.
    
    Args:
        request: The HTTP request object
        pk: The UUID primary key of the author
        
    Returns:
        Rendered author detail template with context data
    """
    author = get_object_or_404(Author, pk=pk)
    
    # Get all books by this author
    books_list = Book.objects.filter(
        authors=author, 
        is_available=True
    ).order_by("-created_at")
    
    # Add pagination (12 books per page)
    paginator = Paginator(books_list, 12)
    page_number = request.GET.get("page")
    books = paginator.get_page(page_number)
    
    context = {
        "author": author,
        "books": books,
    }
    
    return render(request, "books/author_detail.html", context)


def search_ajax(request):
    """
    Provide AJAX search results for live search functionality.
    
    Returns JSON data containing matching books based on a search query.
    Only returns results if the query is at least 3 characters long.
    
    Args:
        request: The HTTP request object with 'q' GET parameter
        
    Returns:
        JsonResponse containing matched books data
    """
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
    """
    Display the About Us page.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered about page template
    """
    return render(request, 'pages/about.html')


def contact(request):
    """
    Display the Contact Us page.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered contact page template
    """
    return render(request, 'pages/contact.html')


@require_POST
def submit_contact_form(request):
    """
    Handle contact form submissions.
    
    Processes form data, stores the message in the database, and sends
    an email notification to the site administrator.
    
    Args:
        request: The HTTP POST request containing form data
        
    Returns:
        JsonResponse indicating success or failure
    """
    try:
        # Parse form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'email': request.POST.get('email'),
                'subject': request.POST.get('subject'),
                'message': request.POST.get('message'),
            }
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False, 
                    'message': f'{field.replace("_", " ").title()} is required.'
                })
        
        # Store in database
        contact_message = ContactMessage.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            subject=data['subject'],
            message=data['message']
        )
        
        # Send email notification (if email is configured)
        try:
            send_mail(
                subject=f'Tales & Tails Contact Form: {data["subject"]}',
                message=f'''
New contact form submission from Tales & Tails website:

From: {data["first_name"]} {data["last_name"]}
Email: {data["email"]}
Subject: {data["subject"]}

Message:
{data["message"]}

---
Submitted at: {contact_message.submitted_at}
Contact ID: {contact_message.id}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Send to yourself
                fail_silently=True,  # Don't break if email fails
            )
        except Exception as email_error:
            # Log email error but don't fail the request
            print(f"Email notification failed: {email_error}")
        
        return JsonResponse({
            'success': True,
            'message': f'Thank you, {data["first_name"]}! Your message has been '
                      f'received. We will get back to you soon.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while sending your message. '
                      'Please try again.'
        })


@require_POST
def newsletter_signup(request):
    """
    Handle newsletter signup requests.
    
    Processes newsletter subscription requests, validates the email address,
    creates or reactivates a subscription, and sends a confirmation email.
    
    Args:
        request: The HTTP POST request containing subscription data
        
    Returns:
        JsonResponse indicating success or failure
    """
    try:
        # Parse form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            email = data.get('email')
        else:
            email = request.POST.get('email')
        
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email address is required.'
            })
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid email address.'
            })
        
        # Create or get newsletter subscription
        newsletter, created = Newsletter.objects.get_or_create(
            email=email,
            defaults={
                'source': 'home_page',
                'is_active': True
            }
        )
        
        # Send confirmation email
        try:
            subject = 'Welcome to Tales & Tails Newsletter'
            text_content = f"""
Thank you for subscribing to Tales & Tails newsletter!

We're excited to have you join our community of dog lovers.
You'll receive updates on our newest books, exclusive offers, and helpful resources for dog owners.

Visit our website to explore our collection: https://talesandtails.com/books/

Woof regards,
The Tales & Tails Team
            """
            
            try:
                html_content = render_to_string('emails/newsletter_welcome.html', {
                    'email': email,
                })
                
                email_message = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email]
                )
                email_message.attach_alternative(html_content, "text/html")
                email_message.send(fail_silently=True)
                
                print(f"✅ Welcome email sent to {email}")
            except Exception as template_error:
                # Fallback to simple text email if template loading fails
                send_mail(
                    subject=subject,
                    message=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True
                )
                print(f"⚠️ HTML email failed, sent plain text email to {email}: "
                     f"{str(template_error)}")
                
        except Exception as email_error:
            print(f"❌ Failed to send confirmation email: {str(email_error)}")
        
        if created:
            return JsonResponse({
                'success': True,
                'message': "Thank you! You've been successfully subscribed to "
                          "our newsletter."
            })
        else:
            if newsletter.is_active:
                return JsonResponse({
                    'success': True,
                    'message': "You're already subscribed to our newsletter!"
                })
            else:
                # Reactivate subscription
                newsletter.is_active = True
                newsletter.save()
                return JsonResponse({
                    'success': True,
                    'message': "Welcome back! Your newsletter subscription has "
                              "been reactivated."
                })
        
    except Exception as e:
        print(f"❌ Newsletter signup error: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        })


# =====================================
# CRUD Views - Staff Only
# =====================================

def is_staff_user(user):
    """
    Check if user is a staff member.
    
    Args:
        user: The user object to check
        
    Returns:
        bool: True if user is staff, False otherwise
    """
    return user.is_staff


@login_required
@user_passes_test(is_staff_user)
def book_manage(request):
    """
    Display the staff book management dashboard.
    
    Provides search functionality and pagination for book management.
    Only accessible to staff users.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered book management template with context data
    """
    search = request.GET.get('search', '')
    books = Book.objects.all()
    
    if search:
        books = books.filter(
            Q(title__icontains=search) | 
            Q(authors__name__icontains=search)
        ).distinct()
    
    books = books.order_by('-created_at')
    paginator = Paginator(books, 20)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    
    return render(request, 'books/manage.html', {
        'books': books,
        'search': search
    })


@login_required
@user_passes_test(is_staff_user)
def book_create(request):
    """
    Create a new book entry.
    
    Handles form submission for creating a new book.
    Only accessible to staff users.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered book form template or redirect to management page
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('books:book_manage')
    else:
        form = BookForm()
    
    return render(request, 'books/form.html', {
        'form': form,
        'title': 'Add New Book',
        'button': 'Create Book'
    })


@login_required
@user_passes_test(is_staff_user)
def book_edit(request, pk):
    """
    Edit an existing book.
    
    Handles form submission for editing book details.
    Only accessible to staff users.
    
    Args:
        request: The HTTP request object
        pk: The UUID primary key of the book
        
    Returns:
        Rendered book form template or redirect to management page
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(
                request, 
                f'Book "{book.title}" has been updated successfully!'
            )
            return redirect('books:book_manage')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'books/form.html', {
        'form': form,
        'book': book,
        'title': f'Edit {book.title}',
        'button': 'Update Book'
    })


@login_required
@user_passes_test(is_staff_user)
def book_remove(request, pk):
    """
    Delete a book with confirmation.
    
    Shows a confirmation page before deleting a book.
    Only accessible to staff users.
    
    Args:
        request: The HTTP request object
        pk: The UUID primary key of the book
        
    Returns:
        Rendered confirmation template or redirect to management page
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('books:book_manage')
    
    return render(request, 'books/delete.html', {'book': book})


# =====================================
# REVIEW Views
# =====================================

@login_required
def review_create(request, book_id):
    """
    Create a new review for a book.
    
    Handles form submission for creating a book review.
    Only allows one review per user per book.
    
    Args:
        request: The HTTP request object
        book_id: The UUID of the book to review
        
    Returns:
        Rendered review form template or redirect to book detail page
    """
    book = get_object_or_404(Book, id=book_id, is_available=True)
    
    # Check if user already reviewed this book
    if book.reviews.filter(user=request.user).exists():
        messages.warning(request, 'You have already reviewed this book.')
        return redirect('books:book_detail', pk=book.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            
            # Update book's average rating
            book.update_average_rating()
            
            messages.success(request, 'Your review has been added successfully!')
            return redirect('books:book_detail', pk=book.id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'book': book,
        'title': f'Review: {book.title}',
    }
    return render(request, 'books/review_form.html', context)


@login_required
def review_edit(request, review_id):
    """
    Edit an existing book review.
    
    Handles form submission for editing a review.
    Users can only edit their own reviews.
    
    Args:
        request: The HTTP request object
        review_id: The ID of the review to edit
        
    Returns:
        Rendered review form template or redirect to book detail page
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book = review.book
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            
            # Update book's average rating
            book.update_average_rating()
            
            messages.success(request, 'Your review has been updated successfully!')
            return redirect('books:book_detail', pk=book.id)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'book': book,
        'review': review,
        'title': f'Edit Review: {book.title}',
        'is_edit': True,
    }
    return render(request, 'books/review_form.html', context)


@login_required
def review_delete(request, review_id):
    """
    Delete a book review.
    
    Shows a confirmation page before deleting a review.
    Users can only delete their own reviews.
    
    Args:
        request: The HTTP request object
        review_id: The ID of the review to delete
        
    Returns:
        Rendered confirmation template or redirect to book detail page
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book = review.book
    
    if request.method == 'POST':
        review.delete()
        
        # Update book's average rating
        book.update_average_rating()
        
        messages.success(request, 'Your review has been deleted.')
        return redirect('books:book_detail', pk=book.id)
    
    context = {
        'review': review,
        'book': book,
    }
    return render(request, 'books/review_delete.html', context)


@login_required
def user_reviews(request):
    """
    Display all reviews written by the current user.
    
    Shows a paginated list of reviews written by the authenticated user.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered user reviews template with context data
    """
    reviews_list = Review.objects.filter(
        user=request.user
    ).select_related("book").order_by("-created_at")
    
    # Add pagination (10 reviews per page)
    paginator = Paginator(reviews_list, 10)
    page_number = request.GET.get("page")
    reviews = paginator.get_page(page_number)
    
    context = {
        "reviews": reviews,
        "total_reviews": reviews_list.count(),
    }
    
    return render(request, "books/user_reviews.html", context)


def test_email(request):
    """
    Test if the email system is configured and working properly.
    
    Sends a test email and displays configuration information.
    Only accessible to staff users.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HTTP response with test results and configuration details
    """
    if not request.user.is_staff:
        return HttpResponse("You don't have permission to access this page.", 
                           status=403)
        
    try:
        # Get the recipient email (default to admin)
        default_recipient = getattr(
            settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL
        )
        recipient = request.GET.get('email', default_recipient)
        
        # Send a test email
        send_mail(
            subject='Tales & Tails - Email System Test',
            message='This is a test email from your Django application. If you '
                   'receive this, your email system is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        # Display success message with settings
        html = f"""
        <h1>Email Test Results</h1>
        <p style="color:green">✅ Test email sent successfully to {recipient}!</p>
        
        <h2>Email Configuration</h2>
        <ul>
            <li><strong>EMAIL_BACKEND:</strong> {settings.EMAIL_BACKEND}</li>
            <li><strong>EMAIL_HOST:</strong> {settings.EMAIL_HOST}</li>
            <li><strong>EMAIL_PORT:</strong> {settings.EMAIL_PORT}</li>
            <li><strong>EMAIL_USE_TLS:</strong> {settings.EMAIL_USE_TLS}</li>
            <li><strong>EMAIL_HOST_USER:</strong> {settings.EMAIL_HOST_USER}</li>
            <li><strong>DEFAULT_FROM_EMAIL:</strong> {settings.DEFAULT_FROM_EMAIL}</li>
        </ul>
        
        <p><a href="/">Return to Homepage</a></p>
        """
        
        return HttpResponse(html)
        
    except Exception as e:
        # Display error message
        html = f"""
        <h1>Email Test Failed</h1>
        <p style="color:red">❌ Error: {str(e)}</p>
        
        <h2>Email Configuration</h2>
        <ul>
            <li><strong>EMAIL_BACKEND:</strong> {settings.EMAIL_BACKEND}</li>
            <li><strong>EMAIL_HOST:</strong> {settings.EMAIL_HOST}</li>
            <li><strong>EMAIL_PORT:</strong> {settings.EMAIL_PORT}</li>
            <li><strong>EMAIL_USE_TLS:</strong> {settings.EMAIL_USE_TLS}</li>
            <li><strong>EMAIL_HOST_USER:</strong> {settings.EMAIL_HOST_USER}</li>
            <li><strong>DEFAULT_FROM_EMAIL:</strong> {settings.DEFAULT_FROM_EMAIL}</li>
        </ul>
        
        <p><a href="/">Return to Homepage</a></p>
        """
        
        return HttpResponse(html)
        