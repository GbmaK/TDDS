from django.shortcuts import render, redirect
from .models import Gasto, Categoria, Presupuesto, Notificacion

def home_view(request):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        gastos = Gasto.objects.filter(usuario_id=usuario_id)
        categorias = Categoria.objects.filter(usuario_id=usuario_id)
        presupuestos = Presupuesto.objects.filter(usuario_id=usuario_id)
        notificaciones = Notificacion.objects.filter(usuario_id=usuario_id)

        context = {
            'gastos': gastos,
            'categorias': categorias,
            'presupuestos': presupuestos,
            'notificaciones': notificaciones,
        }

        return render(request, 'home.html', context)
    else:
        return redirect('login')
    

