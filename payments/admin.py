from django.contrib import admin
from .models import Payment, Pix, Favorite

# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'value', 'date')
    search_fields = ('sender__user__username', 'receiver__user__username')
    list_filter = ('date',)
    ordering = ('-date',)

@admin.register(Pix)
class PixAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'key')
    search_fields = ('user__user__username', 'key')
    list_filter = ('type',)
    ordering = ('user',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__user__username',)
    ordering = ('user',)
