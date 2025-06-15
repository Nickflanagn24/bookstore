"""
URL configuration for bookstore_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

# Import sitemaps when they're created
# from .sitemaps import BookSitemap, StaticViewSitemap

# sitemaps = {
#     'books': BookSitemap,
#     'static': StaticViewSitemap,
# }

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main app URLs (to be added as we develop)
    # path('', include('books.urls')),
    # path('accounts/', include('accounts.urls')),
    # path('orders/', include('orders.urls')),
    # path('reviews/', include('reviews.urls')),
    
    # Home page
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    
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