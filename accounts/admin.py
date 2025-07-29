"""
Admin configuration for the user management system.

This module extends Django's admin functionality to customize how user models
are displayed and managed in the admin interface.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    """
    Form for changing CustomUser details in the admin interface.
    
    This form extends Django's UserChangeForm to work with the CustomUser model.
    """
    class Meta(UserChangeForm.Meta):
        model = CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new CustomUser instances in the admin interface.
    
    This form extends Django's UserCreationForm to work with the CustomUser model.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    
    This class customizes the admin interface for managing CustomUser instances,
    including list displays, filters, fieldsets, and custom admin actions.
    """
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    # Fields to display in the user list
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'dog_owner', 'is_active', 'is_staff', 'date_joined'
    )
    
    # Fields to use for filtering the user list
    list_filter = (
        'is_active', 'is_staff', 'is_superuser', 'dog_owner',
        'training_level', 'newsletter_subscription', 'marketing_emails',
        'date_joined'
    )
    
    # Fields to search
    search_fields = ('username', 'email', 'first_name', 'last_name', 'dog_breed')
    
    # Organize fields in fieldsets for the user edit page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': (
            'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth',
        )}),
        ('Dog Information', {'fields': (
            'dog_owner', 'dog_breed', 'dog_age', 'training_level',
        )}),
        ('Communication Preferences', {'fields': (
            'newsletter_subscription', 'marketing_emails',
        )}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions',
        )}),
        ('Important Dates', {'fields': (
            'last_login', 'date_joined', 'created_at', 'updated_at',
        )}),
    )
    
    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'dog_owner'),
        }),
    )
    
    # Order users by
    ordering = ('-date_joined',)
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at')
    
    # Custom admin actions
    actions = ['activate_users', 'deactivate_users', 'enable_newsletters', 
               'disable_newsletters']
    
    def activate_users(self, request, queryset):
        """
        Custom admin action to activate selected users.
        
        Args:
            request: The HTTP request object
            queryset: The queryset of selected users
            
        Returns:
            None
        """
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users have been activated.')
    
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """
        Custom admin action to deactivate selected users.
        
        Args:
            request: The HTTP request object
            queryset: The queryset of selected users
            
        Returns:
            None
        """
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users have been deactivated.')
    
    deactivate_users.short_description = "Deactivate selected users"
    
    def enable_newsletters(self, request, queryset):
        """
        Custom admin action to subscribe selected users to newsletters.
        
        Args:
            request: The HTTP request object
            queryset: The queryset of selected users
            
        Returns:
            None
        """
        updated = queryset.update(newsletter_subscription=True)
        self.message_user(request, f'{updated} users have been subscribed to newsletters.')
    
    enable_newsletters.short_description = "Subscribe selected users to newsletters"
    
    def disable_newsletters(self, request, queryset):
        """
        Custom admin action to unsubscribe selected users from newsletters.
        
        Args:
            request: The HTTP request object
            queryset: The queryset of selected users
            
        Returns:
            None
        """
        updated = queryset.update(newsletter_subscription=False)
        self.message_user(request, 
                          f'{updated} users have been unsubscribed from newsletters.')
    
    disable_newsletters.short_description = "Unsubscribe selected users from newsletters"
    