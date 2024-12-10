from django.contrib import admin
from .models import Client

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'cpf', 'birth_date', 'cash')
    search_fields = ('user__username', 'cpf', 'phone_number')
    list_filter = ('birth_date',)
    ordering = ('user',)
