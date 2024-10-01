from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            # Crear un nuevo usuario
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # Loguear al usuario
            login(request, user)
            return redirect('home')  # Redirige a una página de inicio
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})
