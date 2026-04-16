from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Usuario

class RegistroUsuarioForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        label="Nombre Completo",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre completo', 'class': 'form-input'})
    )
    correo = forms.EmailField(
        label="Correo Electrónico",
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com', 'class': 'form-input'})
    )
    celular = forms.CharField(
        min_length=10,
        max_length=10,
        label="Celular (10 dígitos)",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '3001234567', 'class': 'form-input'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mínimo 10 caracteres con mayúscula, número y carácter especial', 'class': 'form-input'}),
        label="Contraseña",
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme su contraseña', 'class': 'form-input'}),
        label="Confirmar Contraseña",
        required=True
    )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or not nombre.strip():
            raise forms.ValidationError("El nombre no puede estar vacío.")
        if len(nombre.strip()) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre.strip()

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo or not correo.strip():
            raise forms.ValidationError("El correo no puede estar vacío.")
        # Validar que el correo sea único
        if Usuario.objects.filter(correo=correo).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return correo.strip().lower()

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if not celular or not celular.strip():
            raise forms.ValidationError("El celular no puede estar vacío.")
        if not celular.isdigit():
            raise forms.ValidationError("El celular debe contener solo números.")
        if len(celular) != 10:
            raise forms.ValidationError("El celular debe tener exactamente 10 dígitos.")
        return celular.strip()

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("La contraseña no puede estar vacía.")
        
        # Validaciones de seguridad
        if len(password) < 10:
            raise forms.ValidationError("❌ Mínimo 10 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("❌ Debe contener al menos una letra MAYÚSCULA.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("❌ Debe contener al menos una letra minúscula.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("❌ Debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>\-_=+]', password):
            raise forms.ValidationError("❌ Debe contener un carácter especial (ej. @, #, !, $, *, etc).")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data