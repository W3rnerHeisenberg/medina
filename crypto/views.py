from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import RegistroUsuarioForm
from .models import Usuario

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            try:
                # SEGURIDAD: Transformamos la clave en un Hash irreversible (PBKDF2)
                password_plana = form.cleaned_data['password']
                password_hasheada = make_password(password_plana)
                
                # Crear y guardar el usuario en la base de datos
                usuario = Usuario.objects.create(
                    nombre=form.cleaned_data['nombre'],
                    correo=form.cleaned_data['correo'],
                    celular=form.cleaned_data['celular'],
                    password=password_hasheada
                )
                
                # Guardar en sesión los datos para mostrar en la página de éxito
                request.session['usuario_id'] = usuario.id
                request.session['password_hash'] = password_hasheada
                
                # Redireccionar a la página de éxito
                return redirect('registro_exitoso')
                
            except Exception as e:
                messages.error(request, f"❌ Error al registrar: {str(e)}")
        else:
            # Los errores del formulario se mostrarán automáticamente
            pass
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'registro_form.html', {'form': form})


def registro_exitoso(request):
    # Verificar si hay datos en sesión
    usuario_id = request.session.get('usuario_id')
    password_hash = request.session.get('password_hash')
    
    if not usuario_id or not password_hash:
        # Si no hay datos en sesión, redirigir al registro
        return redirect('registro')
    
    try:
        # Obtener el usuario de la base de datos
        usuario = Usuario.objects.get(id=usuario_id)
        
        context = {
            'usuario': usuario,
            'password_hash': password_hash
        }
        
        # Limpiar la sesión después de mostrar
        del request.session['usuario_id']
        del request.session['password_hash']
        
        return render(request, 'usuario_registrado.html', context)
    except Usuario.DoesNotExist:
        return redirect('registro')