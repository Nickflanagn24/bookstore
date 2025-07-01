from django.core.management.base import BaseCommand
from books.models import Book, Author, Category
from books.services import google_books_api
from decimal import Decimal
import time
import random

class Command(BaseCommand):
    help = 'Populate database with dog books from Google Books API'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=50, help='Number of books to fetch')

    def handle(self, *args, **options):
        limit = options['limit']
        
        # Create dog-related categories
        dog_categories = [
            ('Dog Training', 'Professional dog training techniques and methods'),
            ('Puppy Care', 'Essential care guides for puppies'),
            ('Dog Behavior', 'Understanding canine psychology and behavior'),
            ('Dog Breeds', 'Comprehensive breed guides and information'),
            ('Dog Health', 'Veterinary care and health maintenance'),
            ('Working Dogs', 'Service dogs, therapy dogs, and working breeds'),
            ('Dog Stories', 'Heartwarming tales and dog memoirs'),
            ('Dog Care', 'General dog care and maintenance'),
        ]
        
        for cat_name, description in dog_categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'description': description, 
                    'slug': cat_name.lower().replace(' ', '-').replace('&', 'and')
                }
            )
            if created:
                self.stdout.write(f"✓ Created category: {cat_name}")

        # Dog book search queries for Google Books API
        search_queries = [
            'dog training professional guide',
            'puppy care veterinary guide',
            'dog behavior animal psychology',
            'dog breeds complete guide',
            'canine health veterinary',
            'service dog training',
            'dog obedience training',
            'positive dog training methods',
            'dog agility training',
            'dog nutrition health',
            'understanding dog behavior',
            'raising puppies guide',
            'dog grooming professional',
            'working dogs guide',
            'therapy dog training',
        ]

        books_added = 0
        
        for query in search_queries:
            if books_added >= limit:
                break
                
            self.stdout.write(f"🔍 Searching for: {query}")
            
            # Search Google Books API
            results = google_books_api.search_books(query, max_results=10)
            
            if not results.get('items'):
                self.stdout.write(f"❌ No results for: {query}")
                continue
            
            for item in results.get('items', []):
                if books_added >= limit:
                    break
                    
                try:
                    # Extract book data
                    book_data = google_books_api.extract_book_data(item)
                    
                    # Skip if no title or already exists
                    if not book_data['title']:
                        continue
                        
                    if Book.objects.filter(
                        title__iexact=book_data['title']
                    ).exists():
                        continue
                    
                    # Only include books with images
                    if not book_data.get('cover_image') and not book_data.get('thumbnail'):
                        continue
                    
                    # Create book
                    book = Book.objects.create(
                        title=book_data['title'][:300],  # Truncate if too long
                        subtitle=book_data.get('subtitle', '')[:300] if book_data.get('subtitle') else '',
                        description=book_data.get('description', '')[:2000] if book_data.get('description') else f"Professional guide about {book_data['title']}",
                        google_books_id=book_data.get('google_books_id'),
                        isbn_10=book_data.get('isbn_10'),
                        isbn_13=book_data.get('isbn_13'),
                        thumbnail=book_data.get('thumbnail', ''),
                        cover_image=book_data.get('cover_image', '') or book_data.get('thumbnail', ''),
                        publisher=book_data.get('publisher', '')[:200] if book_data.get('publisher') else '',
                        page_count=book_data.get('page_count'),
                        language=book_data.get('language', 'en'),
                        average_rating=book_data.get('average_rating', 0),
                        ratings_count=book_data.get('ratings_count', 0),
                        price=Decimal(str(random.uniform(12.99, 39.99))).quantize(Decimal('0.01')),
                        stock_quantity=random.randint(5, 50),
                        is_available=True,
                        is_featured=random.choice([True, False, False]),  # 1/3 featured
                    )
                    
                    # Add authors
                    for author_name in book_data.get('authors', []):
                        if author_name:
                            author, created = Author.objects.get_or_create(
                                name=author_name[:200]
                            )
                            book.authors.add(author)
                    
                    # Add categories based on Google categories or search query
                    google_categories = book_data.get('categories', [])
                    categories_added = False
                    
                    for google_cat in google_categories:
                        # Map Google categories to our categories
                        if any(term in google_cat.lower() for term in ['pets', 'dogs', 'animals', 'veterinary']):
                            if 'training' in google_cat.lower() or 'training' in query:
                                cat = Category.objects.get(name='Dog Training')
                                book.categories.add(cat)
                                categories_added = True
                            if 'puppy' in google_cat.lower() or 'puppy' in query:
                                cat = Category.objects.get(name='Puppy Care')
                                book.categories.add(cat)
                                categories_added = True
                            if 'behavior' in google_cat.lower() or 'behavior' in query:
                                cat = Category.objects.get(name='Dog Behavior')
                                book.categories.add(cat)
                                categories_added = True
                            if 'breed' in google_cat.lower() or 'breed' in query:
                                cat = Category.objects.get(name='Dog Breeds')
                                book.categories.add(cat)
                                categories_added = True
                            if 'health' in google_cat.lower() or 'health' in query:
                                cat = Category.objects.get(name='Dog Health')
                                book.categories.add(cat)
                                categories_added = True
                    
                    # Default category assignment based on search query
                    if not categories_added:
                        if 'training' in query:
                            book.categories.add(Category.objects.get(name='Dog Training'))
                        elif 'puppy' in query:
                            book.categories.add(Category.objects.get(name='Puppy Care'))
                        elif 'behavior' in query:
                            book.categories.add(Category.objects.get(name='Dog Behavior'))
                        elif 'breed' in query:
                            book.categories.add(Category.objects.get(name='Dog Breeds'))
                        elif 'health' in query:
                            book.categories.add(Category.objects.get(name='Dog Health'))
                        else:
                            book.categories.add(Category.objects.get(name='Dog Care'))
                    
                    books_added += 1
                    self.stdout.write(f"✅ Added: {book.title[:50]}...")
                    
                    # Small delay to be respectful to Google's API
                    time.sleep(0.1)
                    
                except Exception as e:
                    self.stdout.write(f"❌ Error adding book: {e}")
                    continue
            
            # Delay between searches
            time.sleep(0.5)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {books_added} dog books with images!')
        )
