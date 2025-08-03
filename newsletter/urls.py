from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('confirm/<uuid:token>/', views.confirm_subscription, name='confirm'),
    path('unsubscribe/<uuid:token>/', views.unsubscribe, name='unsubscribe'),
]
