from django import forms
from django.forms import inlineformset_factory
from .models import Tool, ToolImage

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = [
            'name', 
            'description', 
            'category', 
            'price_per_day', 
            'deposit_amount', 
            'is_available', 
            'condition',
            'location'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price_per_day': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'deposit_amount': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }

# Création du formset pour gérer plusieurs images d'outil à la fois
ToolImageFormSet = inlineformset_factory(
    Tool,
    ToolImage,
    fields=['image', 'is_primary'],
    extra=3,  # Nombre de formulaires vides à afficher
    can_delete=True  # Permettre la suppression des images existantes
)