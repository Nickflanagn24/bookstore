from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
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
]
