"""
Google Books API integration service.

This module provides a service class for interacting with the Google Books API,
allowing for book searches, retrieval by ID or ISBN, and data extraction.
"""

import requests
from django.conf import settings
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class GoogleBooksAPI:
    """
    Service class for Google Books API integration.
    
    Provides methods for searching and retrieving book information from the
    Google Books API, with options for different search parameters and
    data extraction.
    """
    
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"
    
    def __init__(self):
        """
        Initialise the API service with the API key from settings.
        """
        self.api_key = settings.GOOGLE_BOOKS_API_KEY
    
    def search_books(
        self, query: str, max_results: int = 10, start_index: int = 0
    ) -> Dict:
        """
        Search for books using Google Books API.
        
        Args:
            query: Search query string
            max_results: Number of results to return (max 40)
            start_index: Starting index for pagination
            
        Returns:
            Dictionary containing search results
        """
        params = {
            'q': query,
            'maxResults': min(max_results, 40),  # Google Books API limit
            'startIndex': start_index,
            'projection': 'full',  # Get full book data
        }
        
        if self.api_key:
            params['key'] = self.api_key
            
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Google Books API request failed: {e}")
            return {'items': [], 'totalItems': 0}
    
    def get_book_by_id(self, google_book_id: str) -> Optional[Dict]:
        """
        Get a specific book by its Google Books ID.
        
        Args:
            google_book_id: Google Books volume ID
            
        Returns:
            Book data dictionary or None if not found
        """
        url = f"{self.BASE_URL}/{google_book_id}"
        params = {}
        
        if self.api_key:
            params['key'] = self.api_key
            
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get book {google_book_id}: {e}")
            return None
    
    def search_by_isbn(self, isbn: str) -> Optional[Dict]:
        """
        Search for a book by ISBN.
        
        Args:
            isbn: ISBN-10 or ISBN-13
            
        Returns:
            Book data dictionary or None if not found
        """
        # Clean ISBN (remove dashes and spaces)
        clean_isbn = isbn.replace('-', '').replace(' ', '')
        
        query = f"isbn:{clean_isbn}"
        results = self.search_books(query, max_results=1)
        
        if results.get('totalItems', 0) > 0:
            return results['items'][0]
        return None
    
    def search_by_title_author(self, title: str, author: str = None) -> Dict:
        """
        Search for books by title and optionally author.
        
        Args:
            title: Book title
            author: Author name (optional)
            
        Returns:
            Dictionary containing search results
        """
        query_parts = [f"intitle:{title}"]
        
        if author:
            query_parts.append(f"inauthor:{author}")
            
        query = " ".join(query_parts)
        return self.search_books(query)
    
    @staticmethod
    def extract_book_data(book_item: Dict) -> Dict:
        """
        Extract and normalise book data from Google Books API response.
        
        Processes the raw API response to extract relevant book information
        in a standardised format suitable for application use.
        
        Args:
            book_item: Single book item from API response
            
        Returns:
            Normalised book data dictionary
        """
        volume_info = book_item.get('volumeInfo', {})
        sale_info = book_item.get('saleInfo', {})
        
        # Extract authors
        authors = volume_info.get('authors', [])
        
        # Extract identifiers
        identifiers = volume_info.get('industryIdentifiers', [])
        isbn_10 = None
        isbn_13 = None
        
        for identifier in identifiers:
            if identifier.get('type') == 'ISBN_10':
                isbn_10 = identifier.get('identifier')
            elif identifier.get('type') == 'ISBN_13':
                isbn_13 = identifier.get('identifier')
        
        # Extract images
        image_links = volume_info.get('imageLinks', {})
        thumbnail = image_links.get('thumbnail', '')
        cover_image = (
            image_links.get('large') or 
            image_links.get('medium') or 
            thumbnail
        )
        
        # Extract categories
        categories = volume_info.get('categories', [])
        main_category = categories[0] if categories else None
        
        # Extract price (if available)
        list_price = sale_info.get('listPrice', {})
        price = list_price.get('amount', 0)
        
        # Extract ratings
        average_rating = volume_info.get('averageRating', 0)
        ratings_count = volume_info.get('ratingsCount', 0)
        
        return {
            'google_books_id': book_item.get('id'),
            'title': volume_info.get('title', ''),
            'subtitle': volume_info.get('subtitle'),
            'authors': authors,
            'publisher': volume_info.get('publisher'),
            'published_date': volume_info.get('publishedDate'),
            'description': volume_info.get('description'),
            'page_count': volume_info.get('pageCount'),
            'language': volume_info.get('language', 'en'),
            'isbn_10': isbn_10,
            'isbn_13': isbn_13,
            'thumbnail': thumbnail,
            'cover_image': cover_image,
            'categories': categories,
            'main_category': main_category,
            'price': price,
            'average_rating': average_rating,
            'ratings_count': ratings_count,
        }


# Convenience instance
google_books_api = GoogleBooksAPI()
