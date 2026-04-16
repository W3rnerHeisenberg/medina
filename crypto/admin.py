from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'celular', 'fecha_registro')
    search_fields = ('nombre', 'correo', 'celular')
    list_filter = ('fecha_registro',)
    readonly_fields = ('password', 'fecha_registro')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'correo', 'celular')
        }),
        ('Seguridad', {
            'fields': ('password',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro',)
        }),
    )
