from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with dog-specific fields"""
    
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
        initial=True,
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
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                 'dog_owner', 'dog_breed', 'newsletter_subscription')

    def __init__(self, *args, **kwargs):
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
    """Form for updating user profile"""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'dog_owner', 'dog_breed', 
                 'dog_age', 'training_level', 'phone_number', 'newsletter_subscription', 
                 'marketing_emails')

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information"""
    
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
    """Custom login form"""
    
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
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
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
        return getattr(self, 'user_cache', None)
