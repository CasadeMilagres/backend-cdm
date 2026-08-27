from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'is_staff', 'is_superuser')
    search_fields = ('nome', 'email')
    list_filter = ('is_staff', 'is_superuser')