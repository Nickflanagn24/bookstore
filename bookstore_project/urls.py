"""
URL configuration for bookstore_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from books.views import home  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Homepage - Tales & Tails home view
    path('', home, name='home'),
    
    # Books app URLs
    path('books/', include('books.urls')),
    
    # Future app URLs
    # path('accounts/', include('accounts.urls')),
    # path('orders/', include('orders.urls')),
    # path('reviews/', include('reviews.urls')),
    
    # SEO URLs
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', 
        content_type='text/plain'
    ), name='robots'),
    
    # Sitemap (will be activated when we have content)
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, 
    #      name='django.contrib.sitemaps.views.sitemap'),
]

# Custom error handlers (to be implemented)
# handler404 = 'books.views.custom_404'
# handler500 = 'books.views.custom_500'

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
