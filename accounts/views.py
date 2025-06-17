from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, ProfileUpdateForm, CustomLoginForm
from .models import CustomUser

def register_view(request):
    """Registration view using function-based approach"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Welcome to Tales & Tails, {user.first_name}! Your account has been created."
            )
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Login view using function-based approach"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Handle remember me
            remember_me = form.cleaned_data.get('remember_me')
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)  # 2 weeks
            
            messages.success(request, f"Welcome back, {user.first_name}!")
            
            # Redirect to next page if specified, otherwise home
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
    else:
        form = CustomLoginForm(request=request)
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """Logout view"""
    if request.user.is_authenticated:
        user_name = request.user.first_name
        logout(request)
        messages.info(request, f"Goodbye, {user_name}! You've been logged out.")
    return redirect('home')

@login_required
def profile_view(request):
    """User profile view - simplified"""
    user = request.user
    
    # Safe context - only include what we know exists
    context = {
        'user': user,
    }
    
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
    """User dashboard view - redirect to appropriate page based on auth status"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    else:
        return redirect('accounts:login')
