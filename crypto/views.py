from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .forms import RegistroUsuarioForm

def registro(request):
    mensaje = ""
    hash_generado = ""
    
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # SEGURIDAD: Transformamos la clave en un Hash irreversible
            password_plana = form.cleaned_data['password']
            hash_generado = make_password(password_plana)
            
            mensaje = f"✅ Usuario {form.cleaned_data['nombre']} validado correctamente."
        else:
            mensaje = "❌ Datos inválidos. Revisa las reglas de seguridad."
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'registro.html', {
        'form': form, 
        'mensaje': mensaje, 
        'hash_ejemplo': hash_generado
    })