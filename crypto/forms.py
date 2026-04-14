from django import forms
import re

class RegistroUsuarioForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre Completo")
    correo = forms.EmailField(label="Correo Electrónico")
    celular = forms.CharField(min_length=10, max_length=10, label="Celular (10 dígitos)")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if not celular.isdigit():
            raise forms.ValidationError("El celular debe contener solo números.")
        return celular

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Reglas de Seguridad del Profe:
        if len(password) < 10:
            raise forms.ValidationError("Mínimo 10 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Falta una letra MAYÚSCULA.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Falta una letra minúscula.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("Falta al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Falta un carácter especial (ej. @, #, !).")
        return password