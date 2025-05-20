from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Order, Reservation, Payment

class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    fields = ['amount', 'payment_method', 'status', 'transaction_id', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    can_delete = False

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'tool_info', 'renter_info', 'dates', 'total_price', 'status', 'has_payment', 'created_at']
    list_filter = ['status', 'start_date', 'end_date', 'created_at']
    search_fields = ['tool__name', 'renter__username', 'renter__email']
    date_hierarchy = 'created_at'
    inlines = [PaymentInline]
    
    fieldsets = (
        ('Informations sur la réservation', {
            'fields': ('tool', 'renter')
        }),
        ('Détails de la location', {
            'fields': ('start_date', 'end_date', 'total_price')
        }),
        ('État', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def tool_info(self, obj):
        return f"{obj.tool.name} (#{obj.tool.id})"
    
    def renter_info(self, obj):
        return f"{obj.renter.username} ({obj.renter.email})"
    
    def dates(self, obj):
        return f"{obj.start_date.strftime('%d/%m/%Y')} - {obj.end_date.strftime('%d/%m/%Y')}"
    
    def has_payment(self, obj):
        try:
            payment = obj.payment
            if payment:
                status_colors = {
                    'pending': 'orange',
                    'completed': 'green',
                    'failed': 'red',
                    'refunded': 'blue'
                }
                color = status_colors.get(payment.status, 'black')
                return format_html('<span style="color: {};">✓ {}</span>', color, payment.get_status_display())
            return format_html('<span style="color: red;">✗</span>')
        except Payment.DoesNotExist:
            return format_html('<span style="color: red;">✗</span>')
    
    tool_info.short_description = "Outil"
    renter_info.short_description = "Locataire"
    dates.short_description = "Période"
    has_payment.short_description = "Paiement"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'reservation_info', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['reservation__tool__name', 'reservation__renter__username', 'transaction_id']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations de paiement', {
            'fields': ('reservation', 'amount', 'payment_method')
        }),
        ('État du paiement', {
            'fields': ('status', 'transaction_id')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def reservation_info(self, obj):
        tool = obj.reservation.tool.name
        renter = obj.reservation.renter.username
        return f"{tool} - {renter} (#{obj.reservation.id})"
    
    reservation_info.short_description = "Réservation"

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    inlines = [CartItemInline]
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'email', 'city', 'phone', 'created_at', 'user_info']
    list_filter = ['created_at', 'city']
    search_fields = ['first_name', 'last_name', 'email', 'address', 'city', 'phone']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations client', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Adresse de livraison', {
            'fields': ('address', 'postal_code', 'city')
        }),
        ('Informations supplémentaires', {
            'fields': ('note', 'user')
        }),
        ('Date', {
            'fields': ('created_at',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def user_info(self, obj):
        return f"{obj.user.username} ({obj.user.email})"
    
    get_full_name.short_description = "Client"
    user_info.short_description = "Utilisateur"

