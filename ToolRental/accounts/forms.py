from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_type = forms.ChoiceField(
        choices=Profile.USER_TYPE_CHOICES,
        label="Type de compte",
        help_text="Choisissez si vous souhaitez louer des outils, proposer vos outils à la location, ou les deux."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'user_type']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'city', 'postal_code', 'profile_picture']
        labels = {
            'phone': 'Téléphone',
            'address': 'Adresse',
            'city': 'Ville',
            'postal_code': 'Code postal',
            'profile_picture': 'Photo de profil'
        }
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Numéro et nom de rue'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Format: +33 6 12 34 56 78'})
        }