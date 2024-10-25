from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Usuarios  # Asegúrate de que sea el nombre correcto

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = Usuarios(  # Cambié 'Usuario' a 'Usuarios'
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email'],
                contraseña=form.cleaned_data['contraseña']  # Guardando la contraseña sin hashear
            )
            usuario.save()
            return redirect('login')  # Asegúrate de que esta URL exista
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
