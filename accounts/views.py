"""
View functions for user authentication and profile management.

This module provides Django view functions for handling user registration,
login, logout, and profile management operations in the accounts application.
"""
from books.models import Review
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import CustomUser


def register_view(request):
    """
    Handle user registration requests.
    
    Processes form submission for creating new user accounts.
    If the user is already authenticated, redirects to home page.
    On successful registration, logs in the user automatically.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Rendered registration template or redirect to home page
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Login the user immediately after registration
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(
                request,
                f"Welcome to Tales & Tails, {user.first_name}! Your account has been created."
            )
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handle user login requests.
    
    Authenticates users against the CustomUser model.
    Performs direct password validation against the stored credentials.
    Redirects authenticated users to the home page.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Rendered login template or redirect to next page
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    error_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            try:
                # Get user by username
                user = CustomUser.objects.get(username=username)
                
                # Check password directly
                if user.check_password(password):
                    if user.is_active:
                        # Login user with explicit backend
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        messages.success(request, f"Welcome back, {user.first_name}!")
                        next_page = request.GET.get('next', 'home')
                        return redirect(next_page)
                    else:
                        error_message = "This account is inactive."
                else:
                    error_message = "Invalid username or password."
            except CustomUser.DoesNotExist:
                error_message = "Invalid username or password."
        else:
            error_message = "Please enter both username and password."
    
    return render(request, 'accounts/login_simple.html', {'error_message': error_message})


def logout_view(request):
    """
    Handle user logout requests.
    
    Logs out the currently authenticated user and displays a farewell message.
    Always redirects to the home page.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Redirect to home page
    """
    if request.user.is_authenticated:
        user_name = request.user.first_name
        logout(request)
        messages.info(request, f"Goodbye, {user_name}! You've been logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    """
    Display user profile information.
    
    Shows user details and activity statistics, including review count.
    Requires user authentication.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Rendered profile template with user context
    """
    context = {
        'user': request.user,
    }
    # Get user reviews count
    user_reviews_count = Review.objects.filter(user=request.user).count() if hasattr(request.user, "reviews") else 0
    context["user_reviews_count"] = user_reviews_count
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """
    Handle user profile editing.
    
    Processes form submission for updating user profile information.
    Requires user authentication.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Rendered profile edit template or redirect to profile view
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})


def dashboard_view(request):
    """
    Handle dashboard view requests.
    
    Redirects authenticated users to their profile page.
    Redirects unauthenticated users to the login page.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: Redirect to profile or login page
    """
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    else:
        return redirect('accounts:login')
        