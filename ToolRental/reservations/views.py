from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Reservation

@login_required
def my_reservations(request):
    # Récupérer les réservations de l'utilisateur connecté
    reservations = Reservation.objects.filter(renter=request.user).order_by('-created_at')
    
    context = {
        'reservations': reservations,
    }
    
    return render(request, 'reservations/my_reservations.html', context)
