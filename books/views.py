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
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    books_queryset = Book.objects.filter(is_available=True).select_related().prefetch_related('authors', 'categories')
    
    # Pagination
    paginator = Paginator(books_queryset, 12)  # Show 12 books per page
    page = request.GET.get('page')
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    
    print(f"DEBUG: Total books: {paginator.count}, Pages: {paginator.num_pages}, Has other pages: {books.has_other_pages()}")
    
    context = {
        'books': books,
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
    
    # Check if user can review and get user review
    user_can_review = book.user_can_review(request.user) if request.user.is_authenticated else False
    user_review = book.get_user_review(request.user) if request.user.is_authenticated else None
    
    context = {
        "book": book,
        "recommendations": recommendations,
        "in_stock": book.is_in_stock,
        "user_can_review": user_can_review,
        "user_review": user_review,
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

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
import json

@require_POST
def submit_contact_form(request):
    """Handle contact form submissions with database storage and email notification"""
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
        from .models import ContactMessage
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
            'message': f'Thank you, {data["first_name"]}! Your message has been received. We will get back to you soon.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while sending your message. Please try again.'
        })

from django.views.decorators.http import require_POST
import json

@require_POST
def newsletter_signup(request):
    """Handle newsletter signup from home page"""
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
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid email address.'
            })
        
        # Create or get newsletter subscription
        from .models import Newsletter
        newsletter, created = Newsletter.objects.get_or_create(
            email=email,
            defaults={
                'source': 'home_page',
                'is_active': True
            }
        )
        
        if created:
            return JsonResponse({
                'success': True,
                'message': f'Thank you! You\'ve been successfully subscribed to our newsletter.'
            })
        else:
            if newsletter.is_active:
                return JsonResponse({
                    'success': True,
                    'message': 'You\'re already subscribed to our newsletter!'
                })
            else:
                # Reactivate subscription
                newsletter.is_active = True
                newsletter.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Welcome back! Your newsletter subscription has been reactivated.'
                })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        })

# =====================================
# CRUD Views - Staff Only
# =====================================
from django.contrib.auth.decorators import user_passes_test
from .forms import BookForm

def is_staff_user(user):
    """Check if user is staff"""
    return user.is_staff

@login_required
@user_passes_test(is_staff_user)
def book_manage(request):
    """Staff book management dashboard"""
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
    """Create new book"""
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
    """Edit existing book"""
    print("=" * 50)
    print("🚀 BOOK_EDIT VIEW CALLED!")
    print(f"📖 PK: {pk}")
    print(f"📤 Method: {request.method}")
    print(f"👤 User: {request.user}")
    print("=" * 50)
    
    book = get_object_or_404(Book, pk=pk)
    print(f"📚 Book found: {book.title}")
    
    if request.method == 'POST':
        print("🔥 POST REQUEST DETECTED!")
        print(f"📝 POST data: {dict(request.POST)}")
        
        form = BookForm(request.POST, instance=book)
        print(f"📋 Form created: {form}")
        
        if form.is_valid():
            print("✅ Form is VALID!")
            book = form.save()
            print(f"💾 Book saved: {book.title}")
            messages.success(request, f'Book "{book.title}" has been updated successfully!')
            print("📤 Redirecting to book_manage...")
            return redirect('books:book_manage')
        else:
            print("❌ Form is INVALID!")
            print(f"🐛 Form errors: {form.errors}")
    else:
        print("�� GET request - showing form")
        form = BookForm(instance=book)
    
    print(f"🎨 Rendering template with book: {book.title}")
    return render(request, 'books/form.html', {
        'form': form,
        'book': book,
        'title': f'Edit {book.title}',
        'button': 'Update Book'
    })

@login_required
@user_passes_test(is_staff_user)
def book_remove(request, pk):
    """Delete book with confirmation"""
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
from .forms import ReviewForm
from .models import Review

@login_required
def review_create(request, book_id):
    """Create a new review for a book"""
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
    """Edit an existing review"""
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
    """Delete a review"""
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
    """Display all reviews by the current user"""
    reviews = Review.objects.filter(user=request.user).select_related('book')
    
    context = {
        'reviews': reviews,
        'total_reviews': reviews.count(),
    }
    return render(request, 'books/user_reviews.html', context)
