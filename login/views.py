from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection  # Para ejecutar consultas SQL directamente

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Consulta para verificar si el email y contraseña coinciden
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_usuario, nombre FROM usuarios WHERE email = %s AND contraseña = %s", [email, password])
            user = cursor.fetchone()

        if user:
            
            request.session['usuario_id'] = user[0]  # Guardar id_usuario en la sesión
            request.session['nombre_usuario'] = user[1]  # Guardar el nombre en la sesión
            return redirect('home')  # Redirige a la página principal después de loguearse
        else:
            messages.error(request, 'Email o contraseña incorrectos.')
            return render(request, 'login.html')

    return render(request, 'login.html')
