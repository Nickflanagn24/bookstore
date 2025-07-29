"""
Form classes for the books application.

This module provides Django form classes for handling book-related operations
such as creating and editing books and book reviews.
"""
from django import forms
from .models import Book, Author, Category, Review


class BookForm(forms.ModelForm):
    """
    Form for book creation and editing operations.
    
    Provides a form interface for creating and updating Book instances,
    with appropriate form widgets and validation. Includes bootstrap
    styling classes for integration with the frontend.
    """
    
    class Meta:
        model = Book
        fields = [
            'title', 'subtitle', 'description', 'publisher',
            'published_date', 'page_count', 'language', 
            'price', 'stock_quantity', 'main_category',
            'thumbnail', 'cover_image', 'is_available', 'is_featured',
            'authors', 'categories'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book title'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtitle (optional)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'publisher': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Publisher'}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'page_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'main_category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Main category'}),
            'thumbnail': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Thumbnail URL'}),
            'cover_image': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Cover image URL'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '4'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '3'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialise the BookForm with custom field configurations.
        
        Sets required fields, input formats, field labels and default values
        for new book instances.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['price'].required = True
        self.fields['language'].required = True
        self.fields['stock_quantity'].required = True
        self.fields['authors'].required = True
        
        # Set the date input format
        self.fields['published_date'].input_formats = ['%Y-%m-%d']
        
        self.fields['is_available'].label = 'Available for purchase'
        self.fields['is_featured'].label = 'Featured book'
        
        # Set defaults for new books only
        if not self.instance.pk:
            self.fields['is_available'].initial = True
            self.fields['language'].initial = 'English'
            self.fields['stock_quantity'].initial = 1


class ReviewForm(forms.ModelForm):
    """
    Form for creating and editing book reviews.
    
    Provides fields for users to submit ratings and comments for books,
    with appropriate validation and Bootstrap styling.
    """
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-select',
                'id': 'rating-select'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Give your review a title...',
                'maxlength': 200
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your thoughts about this book...',
                'rows': 4
            }),
        }
        
    def __init__(self, *args, **kwargs):
        """
        Initialise the ReviewForm with custom field configurations.
        
        Sets field labels, empty label text, and adds Bootstrap validation
        classes based on form errors.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.fields['rating'].empty_label = "Select a rating"
        self.fields['title'].label = "Review Title"
        self.fields['comment'].label = "Your Review"
        
        # Add Bootstrap validation classes
        for field in self.fields.values():
            field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' is-invalid' if self.errors else ''})
            