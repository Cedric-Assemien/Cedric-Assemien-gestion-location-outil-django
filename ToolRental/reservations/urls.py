from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    # URL pour la page "Mes Réservations"
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    # Ces URLs seront à compléter quand les autres vues seront implémentées
    # path('', views.reservation_list, name='list'),
    # path('<int:reservation_id>/', views.reservation_detail, name='detail'),
    # path('create/<int:tool_id>/', views.create_reservation, name='create'),
    # path('<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel'),
    # path('<int:reservation_id>/payment/', views.payment, name='payment'),
]