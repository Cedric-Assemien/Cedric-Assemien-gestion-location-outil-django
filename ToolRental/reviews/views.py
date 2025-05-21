from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from reservations.models import Reservation
from reviews.models import Review

# Create your views here.

@login_required
def submit_review(request, reservation_id):
    """
    Vue pour soumettre un avis sur une location d'outil terminée.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    # Vérifier que l'utilisateur est bien celui qui a fait la réservation
    if request.user != reservation.renter:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': "Vous n'êtes pas autorisé à laisser un avis pour cette réservation."
            })
        messages.error(request, "Vous n'êtes pas autorisé à laisser un avis pour cette réservation.")
        return redirect('reservations:my_reservations')
    
    # Vérifier que la réservation est bien terminée et sans avis existant
    if reservation.status != 'completed' or hasattr(reservation, 'review'):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': "Vous ne pouvez pas laisser un avis pour cette réservation."
            })
        messages.error(request, "Vous ne pouvez pas laisser un avis pour cette réservation.")
        return redirect('reservations:my_reservations')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if not rating or not comment:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': "Veuillez fournir à la fois une note et un commentaire."
                })
            messages.error(request, "Veuillez fournir à la fois une note et un commentaire.")
            return redirect('reservations:my_reservations')
        
        try:
            # Créer l'avis
            review = Review.objects.create(
                reservation=reservation,
                tool=reservation.tool,
                reviewer=request.user,  # L'utilisateur qui soumet l'avis
                rating=int(rating),
                comment=comment
            )
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': "Merci pour votre avis !"
                })
            messages.success(request, "Merci pour votre avis !")
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': f"Une erreur s'est produite lors de l'enregistrement de votre avis: {str(e)}"
                })
            messages.error(request, f"Une erreur s'est produite lors de l'enregistrement de votre avis: {str(e)}")
    
    return redirect('reservations:my_reservations')