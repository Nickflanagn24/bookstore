from books.models import Review
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import CustomUser

def register_view(request):
    """Registration view using function-based approach"""
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
    """Login view using direct password checking"""
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
    """Logout view"""
    if request.user.is_authenticated:
        user_name = request.user.first_name
        logout(request)
        messages.info(request, f"Goodbye, {user_name}! You've been logged out.")
    return redirect('home')

@login_required
def profile_view(request):
    """User profile view"""
    context = {
        'user': request.user,
    }
    # Get user reviews count
    user_reviews_count = Review.objects.filter(user=request.user).count() if hasattr(request.user, "reviews") else 0
    context["user_reviews_count"] = user_reviews_count
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit_view(request):
    """Edit user profile view"""
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
    """User dashboard view"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    else:
        return redirect('accounts:login')
