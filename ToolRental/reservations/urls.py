# reservations/urls.py
from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('create/<int:tool_id>/', views.create_reservation, name='create'),
    path('cart/', views.cart_detail, name='cart'),
   
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('cart/add/<int:tool_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]