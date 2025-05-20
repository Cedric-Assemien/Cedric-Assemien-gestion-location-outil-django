from django.contrib import admin
from django.utils.html import format_html
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'tool_info', 'reviewer_info', 'reservation_info', 'rating_stars', 'comment_short', 'created_at']
    list_filter = ['rating', 'created_at', 'tool__category']
    search_fields = ['tool__name', 'reviewer__username', 'comment']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations sur l\'avis', {
            'fields': ('reservation', 'tool', 'reviewer')
        }),
        ('Évaluation', {
            'fields': ('rating', 'comment')
        }),
        ('Horodatage', {
            'fields': ('created_at',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    def tool_info(self, obj):
        return f"{obj.tool.name} (#{obj.tool.id})"
    
    def reviewer_info(self, obj):
        return f"{obj.reviewer.username} ({obj.reviewer.email})"
    
    def reservation_info(self, obj):
        return f"#{obj.reservation.id}"
    
    def rating_stars(self, obj):
        stars = "★" * obj.rating + "☆" * (5 - obj.rating)
        return format_html('<span style="color: gold;">{}</span>', stars)
    
    def comment_short(self, obj):
        if len(obj.comment) > 50:
            return obj.comment[:50] + "..."
        return obj.comment
    
    tool_info.short_description = "Outil"
    reviewer_info.short_description = "Utilisateur"
    reservation_info.short_description = "Réservation"
    rating_stars.short_description = "Note"
    comment_short.short_description = "Commentaire"
