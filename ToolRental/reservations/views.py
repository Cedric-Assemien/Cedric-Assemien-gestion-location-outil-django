from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Reservation
from .models import Cart, CartItem
import datetime
@login_required
def my_reservations(request):
    # Récupérer les réservations de l'utilisateur connecté
    reservations = Reservation.objects.filter(renter=request.user).order_by('-created_at')
    
    context = {
        'reservations': reservations,
    }
    
    return render(request, 'reservations/my_reservations.html', context)

# reservations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tools.models import Tool
from .models import Cart, CartItem
from django.contrib import messages
import datetime

@login_required
def create_reservation(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    
    # Si la méthode est POST, l'utilisateur a soumis le formulaire de réservation
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        quantity = request.POST.get('quantity', 1)
        
        # Validation des dates et de la disponibilité
        # ... (code de validation) ...
        
        # Création du panier et ajout de l'article
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = CartItem(
            cart=cart,
            tool=tool,
            quantity=quantity,
            start_date=start_date,
            end_date=end_date
        )
        cart_item.save()
        
        messages.success(request, f"{tool.name} a été ajouté à votre panier.")
        return redirect('reservations:cart')
    
    # Si la méthode est GET, afficher le formulaire de réservation
    else:
        # Dates par défaut (aujourd'hui et dans une semaine)
        today = datetime.date.today()
        end_date = today + datetime.timedelta(days=7)
        
        context = {
            'tool': tool,
            'start_date': today,
            'end_date': end_date,
        }
        return render(request, 'reservations/create_reservation.html', context)
    


@login_required
def add_to_cart(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    
    # Vérifier si l'outil est disponible
    if not tool.is_available:
        messages.error(request, "Cet outil n'est plus disponible.")
        return redirect('tools:detail', tool_id=tool_id)
    
    # Récupérer ou créer un panier pour l'utilisateur
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Dates de location (à adapter selon votre formulaire)
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    quantity = int(request.POST.get('quantity', 1))
    
    # Vérifier si l'article est déjà dans le panier
    try:
        cart_item = CartItem.objects.get(cart=cart, tool=tool)
        cart_item.quantity = quantity
        cart_item.start_date = start_date
        cart_item.end_date = end_date
        cart_item.save()
        messages.success(request, "Le panier a été mis à jour.")
    except CartItem.DoesNotExist:
        cart_item = CartItem(
            cart=cart,
            tool=tool,
            quantity=quantity,
            start_date=start_date,
            end_date=end_date
        )
        cart_item.save()
        messages.success(request, "L'outil a été ajouté à votre panier.")
    
    return redirect('reservations:cart')

@login_required
def cart_detail(request):
    """Vue pour afficher le panier"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'reservations/cart.html', {
        'cart': cart,
        'cart_items': cart.items.all()
    })

@login_required
def cart_add(request, tool_id):
    """Ajouter un outil au panier"""
    tool = get_object_or_404(Tool, id=tool_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Logique pour ajouter l'outil au panier
    
    return redirect('reservations:cart')

@login_required
def cart_remove(request, item_id):
    """Supprimer un article du panier"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Article supprimé du panier.")
    return redirect('reservations:cart')

@login_required
def checkout(request):
    """Vue pour le processus de paiement"""
    return render(request, 'reservations/checkout.html')

@login_required
def order_list(request):
    """Liste des commandes de l'utilisateur"""
    return render(request, 'reservations/order_list.html')

@login_required
def order_detail(request, order_id):
    """Détails d'une commande"""
    return render(request, 'reservations/order_detail.html')