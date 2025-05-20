from django.contrib import admin
from django.utils.html import format_html
from .models import Tool, Category, ToolImage

class ToolImageInline(admin.TabularInline):
    model = ToolImage
    extra = 1
    fields = ['image', 'is_primary', 'preview_image']
    readonly_fields = ['preview_image']
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "Aucune image"
    
    preview_image.short_description = "Aperçu"

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'owner_info', 'price_per_day', 'deposit_amount', 'is_available', 'condition', 'created_at']
    list_filter = ['is_available', 'condition', 'category', 'created_at']
    search_fields = ['name', 'description', 'owner__username', 'location']
    date_hierarchy = 'created_at'
    inlines = [ToolImageInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'description', 'category', 'owner')
        }),
        ('Tarifs', {
            'fields': ('price_per_day', 'deposit_amount')
        }),
        ('Détails', {
            'fields': ('is_available', 'condition', 'location')
        }),
    )
    
    def owner_info(self, obj):
        return f"{obj.owner.username} ({obj.owner.email})"
    
    owner_info.short_description = "Propriétaire"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'tool_count', 'description_short']
    search_fields = ['name', 'description']
    
    def tool_count(self, obj):
        return obj.tools.count()
    
    def description_short(self, obj):
        if obj.description and len(obj.description) > 50:
            return obj.description[:50] + "..."
        return obj.description
    
    tool_count.short_description = "Nombre d'outils"
    description_short.short_description = "Description"

@admin.register(ToolImage)
class ToolImageAdmin(admin.ModelAdmin):
    list_display = ['tool', 'is_primary', 'preview']
    list_filter = ['is_primary', 'tool__category']
    search_fields = ['tool__name']
    
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "Aucune image"
    
    preview.short_description = "Aperçu"
