"""
URL configuration for bookstore_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from bookstore_project.sitemaps import sitemaps
from books.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Homepage - Tales & Tails home view
    path('', home, name='home'),
    
    # App URLs
    path('books/', include('books.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    
    # SEO URLs
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Custom error handlers
handler404 = 'django.views.defaults.page_not_found'

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
