"""
Custom form classes for user authentication and profile management.

This module contains forms for user registration, profile updates,
and custom authentication, with specific fields for dog owner profiles.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form with dog-specific fields.
    
    Extends Django's UserCreationForm to include additional fields relevant
    to the application, such as dog ownership details and communication preferences.
    All form fields are styled with Bootstrap classes.
    """
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    dog_owner = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    dog_breed = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Golden Retriever, Mixed Breed'
        })
    )
    newsletter_subscription = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                 'dog_owner', 'dog_breed', 'newsletter_subscription')

    def __init__(self, *args, **kwargs):
        """
        Initialise the form and set custom widget attributes.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })

    def save(self, commit=True):
        """
        Save the form data to create a new user.
        
        Args:
            commit (bool): Whether to save the user to the database
            
        Returns:
            CustomUser: The newly created user object
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.dog_owner = self.cleaned_data['dog_owner']
        user.dog_breed = self.cleaned_data['dog_breed']
        user.newsletter_subscription = self.cleaned_data['newsletter_subscription']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating user profile information.
    
    Extends Django's UserChangeForm to include custom user fields relevant
    to the application's profile management functionality.
    """
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'dog_owner', 'dog_breed', 
                 'dog_age', 'training_level', 'phone_number', 'newsletter_subscription', 
                 'marketing_emails')

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    
    Provides fields for users to update their personal details, dog information,
    and communication preferences. All form fields are styled with Bootstrap classes.
    """
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'dog_owner', 'dog_breed', 'dog_age', 
                 'training_level', 'phone_number', 'newsletter_subscription', 
                 'marketing_emails')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dog_breed': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'dog_age': forms.Select(attrs={'class': 'form-select'}),
            'training_level': forms.Select(attrs={'class': 'form-select'}),
            'dog_owner': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'newsletter_subscription': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'marketing_emails': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CustomLoginForm(forms.Form):
    """
    Custom login form that authenticates users using email instead of username.
    
    Provides fields for email-based authentication with additional options like
    remember me functionality. All form fields are styled with Bootstrap classes.
    """
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        """
        Initialise the form and store the request object.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments with optional 'request' parameter
        """
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Validate the form data and authenticate the user.
        
        Retrieves the CustomUser by email and attempts authentication.
        
        Returns:
            dict: The cleaned data
            
        Raises:
            ValidationError: If authentication fails or account is inactive
        """
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
                self.user_cache = authenticate(self.request, username=user.username, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError("Invalid email or password.")
                elif not self.user_cache.is_active:
                    raise forms.ValidationError("This account is inactive.")
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Invalid email or password.")

        return self.cleaned_data

    def get_user(self):
        """
        Return the authenticated user.
        
        Returns:
            CustomUser: The authenticated user or None
        """
        return getattr(self, 'user_cache', None)
        