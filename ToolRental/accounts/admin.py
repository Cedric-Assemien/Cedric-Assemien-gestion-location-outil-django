from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profils"
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_type')
    list_filter = ('is_staff', 'is_superuser', 'profile__user_type')
    search_fields = ['username', 'first_name', 'last_name', 'email', 'profile__phone']
    
    def get_user_type(self, obj):
        return obj.profile.get_user_type_display()
    
    get_user_type.short_description = 'Type d\'utilisateur'
    get_user_type.admin_order_field = 'profile__user_type'

# Ré-enregistrer le modèle User avec notre classe UserAdmin personnalisée
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone', 'city', 'postal_code']
    list_filter = ['user_type', 'city']
    search_fields = ['user__username', 'user__email', 'phone', 'address', 'city']
    readonly_fields = ['user']
