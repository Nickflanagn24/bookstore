from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Cart management URLs
    path('', views.cart_detail, name='cart_detail'),
    path('add/<uuid:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<uuid:item_id>/', views.update_cart_item, name='update_item'),
    path('remove/<uuid:item_id>/', views.remove_from_cart, name='remove_item'),
    path('clear/', views.clear_cart, name='clear_cart'),
]