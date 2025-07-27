from django.urls import path
from . import views
from .email_preview import preview_email_template
from .test_email_public import test_email_public

app_name = 'books'

urlpatterns = [
    path('test-email-public/', test_email_public, name='test_email_public'),
    path('test-email/', views.test_email, name='test_email'),
    # Main book pages
    path('', views.book_list, name='book_list'),
    path('book/<uuid:pk>/', views.book_detail, name='book_detail'),
    
    # Category and author pages
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('author/<uuid:pk>/', views.author_detail, name='author_detail'),
    
    # AJAX endpoints
    path('search/ajax/', views.search_ajax, name='search_ajax'),
    
    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/submit/', views.submit_contact_form, name='submit_contact_form'),
    path("newsletter/signup/", views.newsletter_signup, name="newsletter_signup"),
    
    # Staff CRUD URLs
    path('manage/', views.book_manage, name='book_manage'),
    path('add/', views.book_create, name='book_create'),
    path('book/<uuid:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<uuid:pk>/delete/', views.book_remove, name='book_remove'),
    
    # Review URLs
    path('book/<uuid:book_id>/review/add/', views.review_create, name='review_create'),
    path('review/<int:review_id>/edit/', views.review_edit, name='review_edit'),
    path('review/<int:review_id>/delete/', views.review_delete, name='review_delete'),
    path('my-reviews/', views.user_reviews, name='user_reviews'),
    
    # Email preview URLs (only for development)
    path('email/preview/order/', lambda request: preview_email_template(request, 'order_confirmation'), name='preview_order_email'),
    path('email/preview/shipping/', lambda request: preview_email_template(request, 'shipping_notification'), name='preview_shipping_email'),
    path('email/preview/password/', lambda request: preview_email_template(request, 'password_reset'), name='preview_password_email'),
]
