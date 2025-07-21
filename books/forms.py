from django import forms
from .models import Book, Author, Category

class BookForm(forms.ModelForm):
    """Form for Book CRUD operations"""
    
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
