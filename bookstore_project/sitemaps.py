from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.urls import reverse
from books.models import Book

# Define your sitemaps
book_info = {
    'queryset': Book.objects.all(),
    'date_field': 'created_at',  # Adjust if your field name is different
}

# Static pages sitemap
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home', 'books:book_list', 'books:about', 'books:contact']

    def location(self, item):
        return reverse(item)

# Create sitemaps dictionary
sitemaps = {
    'books': GenericSitemap(book_info, priority=0.7),
    'static': StaticViewSitemap(),
}
