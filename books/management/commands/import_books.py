"""
Management command to import books from Google Books API
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from books.services import google_books_api
from books.models import Book, Author, Category
from django.utils.text import slugify
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import books from Google Books API'

    def add_arguments(self, parser):
        parser.add_argument(
            'query',
            type=str,
            help='Search query for books to import'
        )
        parser.add_argument(
            '--max-results',
            type=int,
            default=10,
            help='Maximum number of books to import (default: 10)'
        )
        parser.add_argument(
            '--default-price',
            type=float,
            default=19.99,
            help='Default price for books without price data (default: 19.99)'
        )

    def handle(self, *args, **options):
        query = options['query']
        max_results = options['max_results']
        default_price = Decimal(str(options['default_price']))

        self.stdout.write(
            self.style.SUCCESS(f'Importing books for query: "{query}"')
        )

        # Search for books
        results = google_books_api.search_books(query, max_results=max_results)
        
        if not results.get('items'):
            self.stdout.write(
                self.style.WARNING('No books found for the given query.')
            )
            return

        imported_count = 0
        skipped_count = 0

        for book_item in results['items']:
            try:
                with transaction.atomic():
                    book_data = google_books_api.extract_book_data(book_item)
                    
                    # Skip if no title
                    if not book_data['title']:
                        skipped_count += 1
                        continue
                    
                    # Check if book already exists
                    if Book.objects.filter(google_books_id=book_data['google_books_id']).exists():
                        self.stdout.write(f"Skipping existing book: {book_data['title']}")
                        skipped_count += 1
                        continue
                    
                    # Create or get authors
                    authors = []
                    for author_name in book_data['authors']:
                        author, created = Author.objects.get_or_create(
                            name=author_name,
                            defaults={'biography': f'Author of {book_data["title"]}'}
                        )
                        authors.append(author)
                    
                    # Create or get categories
                    categories = []
                    for category_name in book_data['categories']:
                        category, created = Category.objects.get_or_create(
                            name=category_name,
                            defaults={'slug': slugify(category_name)}
                        )
                        categories.append(category)
                    
                    # Create book
                    book = Book.objects.create(
                        google_books_id=book_data['google_books_id'],
                        title=book_data['title'],
                        subtitle=book_data['subtitle'],
                        publisher=book_data['publisher'],
                        published_date=self._parse_date(book_data['published_date']),
                        description=book_data['description'],
                        page_count=book_data['page_count'],
                        language=book_data['language'],
                        isbn_10=book_data['isbn_10'],
                        isbn_13=book_data['isbn_13'],
                        thumbnail=book_data['thumbnail'],
                        cover_image=book_data['cover_image'],
                        main_category=book_data['main_category'],
                        price=Decimal(str(book_data['price'])) if book_data['price'] > 0 else default_price,
                        stock_quantity=10,  # Default stock
                        is_available=True,
                        average_rating=book_data['average_rating'],
                        ratings_count=book_data['ratings_count'],
                    )
                    
                    # Add relationships
                    book.authors.set(authors)
                    book.categories.set(categories)
                    
                    self.stdout.write(f"Imported: {book.title}")
                    imported_count += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error importing book: {e}')
                )
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Import completed! Imported: {imported_count}, Skipped: {skipped_count}'
            )
        )

    def _parse_date(self, date_string):
        """Parse various date formats from Google Books"""
        if not date_string:
            return None
        
        try:
            # Try different date formats
            from datetime import datetime
            
            # Try YYYY-MM-DD
            if len(date_string) == 10:
                return datetime.strptime(date_string, '%Y-%m-%d').date()
            # Try YYYY-MM
            elif len(date_string) == 7:
                return datetime.strptime(date_string + '-01', '%Y-%m-%d').date()
            # Try YYYY
            elif len(date_string) == 4:
                return datetime.strptime(date_string + '-01-01', '%Y-%m-%d').date()
        except:
            pass
        
        return None