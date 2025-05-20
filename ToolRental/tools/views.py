from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.utils import timezone
from django.contrib import messages
from .models import Tool, Category, ToolImage
from .forms import ToolForm, ToolImageFormSet

def home(request):
    # Récupération des outils à afficher sur la page d'accueil
    new_tools = Tool.objects.filter(is_available=True).order_by('-created_at')[:6]
    popular_tools = Tool.objects.filter(is_available=True).annotate(
        reservation_count=Count('reservations')).order_by('-reservation_count')[:6]
    rated_tools = Tool.objects.filter(is_available=True).annotate(
        avg_rating=Avg('reviews__rating')).filter(avg_rating__isnull=False).order_by('-avg_rating')[:6]
    
    # Récupération des catégories mises en avant
    featured_categories = Category.objects.all()[:3]
    
    # Récupération des avis pour les témoignages
    from reviews.models import Review
    testimonials = Review.objects.filter(rating__gte=4).order_by('-created_at')[:4]
    
    context = {
        'new_tools': new_tools,
        'popular_tools': popular_tools,
        'rated_tools': rated_tools,
        'featured_categories': featured_categories,
        'testimonials': testimonials,
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    
    return render(request, 'tools/home.html', context)

def tool_list(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('query')
    
    tools = Tool.objects.filter(is_available=True)
    
    if category_id:
        tools = tools.filter(category_id=category_id)
    
    if search_query:
        tools = tools.filter(name__icontains=search_query) | tools.filter(description__icontains=search_query)
    
    context = {
        'tools': tools,
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
        'selected_category': int(category_id) if category_id else None,
        'search_query': search_query,
    }
    
    return render(request, 'tools/tool_list.html', context)

def tool_detail(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    
    # Vérifier si l'utilisateur a déjà loué cet outil
    user_has_rented = False
    user_has_reviewed = False
    
    if request.user.is_authenticated:
        from reservations.models import Reservation
        user_rentals = Reservation.objects.filter(
            renter=request.user,
            tool=tool,
            status__in=['completed', 'confirmed']
        ).exists()
        user_has_rented = user_rentals
        
        from reviews.models import Review
        user_has_reviewed = Review.objects.filter(
            reviewer=request.user,
            tool=tool
        ).exists()
    
    # Récupérer les outils similaires
    related_tools = Tool.objects.filter(
        category=tool.category,
        is_available=True
    ).exclude(id=tool.id)[:4]
    
    context = {
        'tool': tool,
        'related_tools': related_tools,
        'user_has_rented': user_has_rented,
        'user_has_reviewed': user_has_reviewed,
        'today': timezone.now(),
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    
    return render(request, 'tools/tool_detail.html', context)

@login_required
def add_tool(request):
    # Vérifier si l'utilisateur est propriétaire
    if request.user.profile.user_type != 'proprietaire':
        messages.error(request, "Vous devez être inscrit en tant que propriétaire pour ajouter des outils.")
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = ToolForm(request.POST)
        formset = ToolImageFormSet(request.POST, request.FILES, prefix='images')
        
        if form.is_valid() and formset.is_valid():
            tool = form.save(commit=False)
            tool.owner = request.user
            tool.save()
            
            # Enregistrement des images
            instances = formset.save(commit=False)
            for instance in instances:
                instance.tool = tool
                instance.save()
            
            messages.success(request, f"L'outil {tool.name} a été ajouté avec succès !")
            return redirect('tools:detail', tool_id=tool.id)
    else:
        form = ToolForm()
        formset = ToolImageFormSet(prefix='images')
    
    context = {
        'form': form,
        'formset': formset,
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    
    return render(request, 'tools/tool_add.html', context)

@login_required
def my_tools(request):
    tools = Tool.objects.filter(owner=request.user)
    
    context = {
        'tools': tools,
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    
    return render(request, 'tools/my_tools.html', context)

@login_required
def edit_tool(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id, owner=request.user)
    
    if request.method == 'POST':
        form = ToolForm(request.POST, instance=tool)
        formset = ToolImageFormSet(request.POST, request.FILES, prefix='images', instance=tool)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            messages.success(request, f"L'outil {tool.name} a été mis à jour avec succès !")
            return redirect('tools:detail', tool_id=tool.id)
    else:
        form = ToolForm(instance=tool)
        formset = ToolImageFormSet(prefix='images', instance=tool)
    
    context = {
        'form': form,
        'formset': formset,
        'tool': tool,
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    
    return render(request, 'tools/tool_edit.html', context)

def category_list(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
        'footer_categories': Category.objects.all()[:5],
    }
    
    return render(request, 'tools/category_list.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    tools = Tool.objects.filter(category=category, is_available=True)
    
    context = {
        'category': category,
        'tools': tools,
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    
    return render(request, 'tools/category_detail.html', context)


# Pages statiques
def about(request):
    context = {
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    return render(request, 'tools/about.html', context)

def contact(request):
    context = {
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    return render(request, 'tools/contact.html', context)

def how_it_works(request):
    context = {
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    return render(request, 'tools/how_it_works.html', context)

def terms(request):
    context = {
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    return render(request, 'tools/terms.html', context)

def privacy(request):
    context = {
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    return render(request, 'tools/privacy.html', context)

def faq(request):
    context = {
        'categories': Category.objects.all(),
        'footer_categories': Category.objects.all()[:5],
    }
    return render(request, 'tools/faq.html', context)