from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Tool(models.Model):
    CONDITION_CHOICES = [
        ('neuf', 'Neuf'),
        ('excellent', 'Excellent'),
        ('bon', 'Bon'),
        ('usage', 'Usagé'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tools')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tools')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='bon')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255, blank=True, null=True)  # Localisation de l'outil pour la recherche
    
    def __str__(self):
        return self.name

class ToolImage(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tools/')
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.tool.name}"
