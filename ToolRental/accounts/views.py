from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Mettre à jour le type d'utilisateur dans le profil
            user_type = form.cleaned_data.get('user_type')
            profile = Profile.objects.get(user=user)
            profile.user_type = user_type
            profile.save()
            
            messages.success(request, f'Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Votre profil a été mis à jour avec succès !')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    # Récupérer les réservations de l'utilisateur
    from reservations.models import Reservation
    reservations = Reservation.objects.filter(renter=request.user).order_by('-created_at')[:3]
    
    # Pour les propriétaires, récupérer aussi les outils
    is_proprietaire = request.user.profile.user_type == 'proprietaire'
    tools = None
    if is_proprietaire:
        from tools.models import Tool
        tools = Tool.objects.filter(owner=request.user).order_by('-created_at')[:3]
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'reservations': reservations,
        'tools': tools,
        'is_proprietaire': is_proprietaire,
    }
    
    return render(request, 'accounts/profile.html', context)

def owner_profile(request, owner_id):
    owner = get_object_or_404(User, id=owner_id)
    
    # Récupérer les outils du propriétaire
    from tools.models import Tool
    tools = Tool.objects.filter(owner=owner, is_available=True)
    
    # Récupérer les avis sur les outils du propriétaire
    from reviews.models import Review
    reviews = Review.objects.filter(tool__owner=owner).order_by('-created_at')[:5]
    
    # Calculer la note moyenne
    avg_rating = reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0
    
    context = {
        'owner': owner,
        'tools': tools,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    
    return render(request, 'accounts/owner_profile.html', context)
