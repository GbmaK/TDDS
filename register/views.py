from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Usuario  # Asegúrate de importar tu modelo

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Crear una nueva instancia del modelo Usuario y guardar
            usuario = Usuario(
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email'],
                contraseña=form.cleaned_data['contraseña']  # Aquí puedes agregar el hash en producción
            )
            usuario.save()  # Esto debería funcionar ahora
            return redirect('login')  # Redirigir a la página de login o donde desees
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
