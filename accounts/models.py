from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    # Dog-related profile fields
    dog_owner = models.BooleanField(default=True, help_text="Do you own a dog?")
    dog_breed = models.CharField(max_length=100, blank=True, null=True, help_text="What breed is your dog?")
    dog_age = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        choices=[
            ('puppy', 'Puppy (0-1 year)'),
            ('young', 'Young (1-3 years)'),
            ('adult', 'Adult (3-7 years)'),
            ('senior', 'Senior (7+ years)'),
        ],
        help_text="Age of your dog"
    )
    training_level = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('professional', 'Professional Trainer'),
        ],
        help_text="Your training experience level"
    )
    
    # Profile fields
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Newsletter and communication preferences
    newsletter_subscription = models.BooleanField(
        default=True, 
        help_text="Receive Tales & Tails newsletter and book recommendations"
    )
    marketing_emails = models.BooleanField(
        default=False,
        help_text="Receive promotional emails and special offers"
    )
    
    # Account metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email as the unique identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def dog_info(self):
        """Return formatted dog information"""
        if not self.dog_owner:
            return "No dog"
        
        info_parts = []
        if self.dog_breed:
            info_parts.append(self.dog_breed)
        if self.dog_age:
            info_parts.append(f"({self.get_dog_age_display()})")
        
        return " ".join(info_parts) if info_parts else "Dog owner"
    
    def get_recommended_categories(self):
        """Get book categories recommended for this user"""
        from books.models import Category
        
        recommendations = []
        
        if self.dog_age == 'puppy':
            recommendations.extend(['Puppy Training', 'Puppy Care'])
        elif self.training_level == 'beginner':
            recommendations.extend(['Dog Training', 'Dog Behavior'])
        elif self.training_level == 'professional':
            recommendations.extend(['Professional Dog Training', 'Service Dogs'])
        
        if self.dog_breed:
            recommendations.append('Dog Breeds')
        
        return Category.objects.filter(name__in=recommendations)