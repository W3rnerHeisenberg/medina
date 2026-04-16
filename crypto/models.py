from django.db import models
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    correo = models.EmailField(unique=True, null=False, blank=False)
    celular = models.CharField(max_length=10, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.correo})"
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-fecha_registro']
