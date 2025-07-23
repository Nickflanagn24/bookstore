from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Author(models.Model):
    """Author model for book authors"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True, null=True)
    photo = models.URLField(blank=True, null=True, help_text="Author photo URL")
    google_books_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def update_average_rating(self):
        """Calculate and update average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            self.average_rating = total_rating / len(reviews)
            self.ratings_count = len(reviews)
        else:
            self.average_rating = 0
            self.ratings_count = 0
        self.save(update_fields=["average_rating", "ratings_count"])
    
    @property
    def star_display(self):
        """Return average rating as visual stars"""
        if self.average_rating > 0:
            full_stars = int(self.average_rating)
            half_star = 1 if (self.average_rating - full_stars) >= 0.5 else 0
            empty_stars = 5 - full_stars - half_star
            return "⭐" * full_stars + ("⭐" if half_star else "") + "☆" * empty_stars
        return "☆☆☆☆☆"
    
    def user_can_review(self, user):
        """Check if user can leave a review for this book"""
        if not user.is_authenticated:
            return False
        return not self.reviews.filter(user=user).exists()
    
    def get_user_review(self, user):
        """Get user's review for this book if exists"""
        if user.is_authenticated:
            return self.reviews.filter(user=user).first()
        return None

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:author_detail', kwargs={'pk': self.pk})


class Category(models.Model):
    """Book category model"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def update_average_rating(self):
        """Calculate and update average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            self.average_rating = total_rating / len(reviews)
            self.ratings_count = len(reviews)
        else:
            self.average_rating = 0
            self.ratings_count = 0
        self.save(update_fields=["average_rating", "ratings_count"])
    
    @property
    def star_display(self):
        """Return average rating as visual stars"""
        if self.average_rating > 0:
            full_stars = int(self.average_rating)
            half_star = 1 if (self.average_rating - full_stars) >= 0.5 else 0
            empty_stars = 5 - full_stars - half_star
            return "⭐" * full_stars + ("⭐" if half_star else "") + "☆" * empty_stars
        return "☆☆☆☆☆"
    
    def user_can_review(self, user):
        """Check if user can leave a review for this book"""
        if not user.is_authenticated:
            return False
        return not self.reviews.filter(user=user).exists()
    
    def get_user_review(self, user):
        """Get user's review for this book if exists"""
        if user.is_authenticated:
            return self.reviews.filter(user=user).first()
        return None

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:category_detail', kwargs={'slug': self.slug})


class Book(models.Model):
    """Book model with Google Books API integration"""
    
    # Book identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    google_books_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    isbn_10 = models.CharField(max_length=10, blank=True, null=True)
    isbn_13 = models.CharField(max_length=13, blank=True, null=True)
    
    # Basic book information
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.CharField(max_length=200, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    
    # Book content
    description = models.TextField(blank=True, null=True)
    page_count = models.PositiveIntegerField(blank=True, null=True)
    language = models.CharField(max_length=10, default='en')
    
    # Images and media
    thumbnail = models.URLField(blank=True, null=True, help_text="Small book cover image URL")
    cover_image = models.URLField(blank=True, null=True, help_text="Large book cover image URL")
    
    # Categories and classification
    categories = models.ManyToManyField(Category, related_name='books', blank=True)
    main_category = models.CharField(max_length=200, blank=True, null=True)
    
    # E-commerce fields
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Ratings and reviews
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    ratings_count = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Book"
        verbose_name_plural = "Books"
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['google_books_id']),
            models.Index(fields=['isbn_13']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_available']),
        ]

    def update_average_rating(self):
        """Calculate and update average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            self.average_rating = total_rating / len(reviews)
            self.ratings_count = len(reviews)
        else:
            self.average_rating = 0
            self.ratings_count = 0
        self.save(update_fields=["average_rating", "ratings_count"])
    
    @property
    def star_display(self):
        """Return average rating as visual stars"""
        if self.average_rating > 0:
            full_stars = int(self.average_rating)
            half_star = 1 if (self.average_rating - full_stars) >= 0.5 else 0
            empty_stars = 5 - full_stars - half_star
            return "⭐" * full_stars + ("⭐" if half_star else "") + "☆" * empty_stars
        return "☆☆☆☆☆"
    
    def user_can_review(self, user):
        """Check if user can leave a review for this book"""
        if not user.is_authenticated:
            return False
        return not self.reviews.filter(user=user).exists()
    
    def get_user_review(self, user):
        """Get user's review for this book if exists"""
        if user.is_authenticated:
            return self.reviews.filter(user=user).first()
        return None

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'pk': self.pk})

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0 and self.is_available

    @property
    def authors_list(self):
        return ", ".join([author.name for author in self.authors.all()])

    def get_main_author(self):
        return self.authors.first()

    @property
    def display_price(self):
        return f"£{self.price:.2f}"
class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def update_average_rating(self):
        """Calculate and update average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            self.average_rating = total_rating / len(reviews)
            self.ratings_count = len(reviews)
        else:
            self.average_rating = 0
            self.ratings_count = 0
        self.save(update_fields=["average_rating", "ratings_count"])
    
    @property
    def star_display(self):
        """Return average rating as visual stars"""
        if self.average_rating > 0:
            full_stars = int(self.average_rating)
            half_star = 1 if (self.average_rating - full_stars) >= 0.5 else 0
            empty_stars = 5 - full_stars - half_star
            return "⭐" * full_stars + ("⭐" if half_star else "") + "☆" * empty_stars
        return "☆☆☆☆☆"
    
    def user_can_review(self, user):
        """Check if user can leave a review for this book"""
        if not user.is_authenticated:
            return False
        return not self.reviews.filter(user=user).exists()
    
    def get_user_review(self, user):
        """Get user's review for this book if exists"""
        if user.is_authenticated:
            return self.reviews.filter(user=user).first()
        return None

    def __str__(self):
        return f"{self.subject} - {self.email}"

class Newsletter(models.Model):
    """Newsletter subscription model"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    source = models.CharField(max_length=50, default='website', help_text="Where they signed up")
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
    
    def update_average_rating(self):
        """Calculate and update average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            self.average_rating = total_rating / len(reviews)
            self.ratings_count = len(reviews)
        else:
            self.average_rating = 0
            self.ratings_count = 0
        self.save(update_fields=["average_rating", "ratings_count"])
    
    @property
    def star_display(self):
        """Return average rating as visual stars"""
        if self.average_rating > 0:
            full_stars = int(self.average_rating)
            half_star = 1 if (self.average_rating - full_stars) >= 0.5 else 0
            empty_stars = 5 - full_stars - half_star
            return "⭐" * full_stars + ("⭐" if half_star else "") + "☆" * empty_stars
        return "☆☆☆☆☆"
    
    def user_can_review(self, user):
        """Check if user can leave a review for this book"""
        if not user.is_authenticated:
            return False
        return not self.reviews.filter(user=user).exists()
    
    def get_user_review(self, user):
        """Get user's review for this book if exists"""
        if user.is_authenticated:
            return self.reviews.filter(user=user).first()
        return None

    def __str__(self):
        return f"{self.email} - {'Active' if self.is_active else 'Inactive'}"

class Review(models.Model):
    """Review model for book ratings and comments"""
    RATING_CHOICES = [(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('book', 'user')  # One review per user per book
        ordering = ['-created_at']
    
    def update_average_rating(self):
        """Calculate and update average rating from reviews"""
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            self.average_rating = total_rating / len(reviews)
            self.ratings_count = len(reviews)
        else:
            self.average_rating = 0
            self.ratings_count = 0
        self.save(update_fields=["average_rating", "ratings_count"])
    
    @property
    def star_display(self):
        """Return average rating as visual stars"""
        if self.average_rating > 0:
            full_stars = int(self.average_rating)
            half_star = 1 if (self.average_rating - full_stars) >= 0.5 else 0
            empty_stars = 5 - full_stars - half_star
            return "⭐" * full_stars + ("⭐" if half_star else "") + "☆" * empty_stars
        return "☆☆☆☆☆"
    
    def user_can_review(self, user):
        """Check if user can leave a review for this book"""
        if not user.is_authenticated:
            return False
        return not self.reviews.filter(user=user).exists()
    
    def get_user_review(self, user):
        """Get user's review for this book if exists"""
        if user.is_authenticated:
            return self.reviews.filter(user=user).first()
        return None

    def __str__(self):
        return f'{self.user.username} - {self.book.title} ({self.rating}⭐)'
    
    @property
    def star_display(self):
        """Return stars as visual representation"""
        full_stars = '⭐' * self.rating
        empty_stars = '☆' * (5 - self.rating)
        return full_stars + empty_stars
