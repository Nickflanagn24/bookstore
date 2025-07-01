from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from books.models import Book, Category, Author

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'books:book_list', 'books:about', 'books:contact']

    def location(self, item):
        return reverse(item)

class BookSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Book.objects.filter(is_available=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()

class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

class AuthorSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Author.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

# Sitemap dictionary
sitemaps = {
    'static': StaticViewSitemap,
    'books': BookSitemap,
    'categories': CategorySitemap,
    'authors': AuthorSitemap,
}
