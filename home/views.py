from django.shortcuts import render, redirect
from .models import Gastos, Categorias, Presupuestos, Notificaciones
import datetime

def home_view(request):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        gastos = Gastos.objects.filter(usuario_id=usuario_id)
        categorias = Categorias.objects.filter(usuario_id=usuario_id)
        presupuestos = Presupuestos.objects.filter(usuario_id=usuario_id)
        notificaciones = Notificaciones.objects.filter(usuario_id=usuario_id)

        context = {
            'gastos': gastos,
            'categorias': categorias,
            'presupuestos': presupuestos,
            'notificaciones': notificaciones,
        }

        print('holaaaaaaaaaaaaaaaaaa',context)

        return render(request, 'home.html', context)
    else:
        return redirect('login')



def nuevo_gasto(request):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        categorias = Categorias.objects.filter(usuario_id=usuario_id)

        print(usuario_id)
        print(categorias)
        if request.method == 'POST':
            # Aquí deberías manejar la creación del nuevo gasto
            titulo = request.POST.get('titulo')
            categoria_id = request.POST.get('categoria')
            monto = request.POST.get('monto')
            descripcion = request.POST.get('descripcion')

            nuevo_gasto = Gastos(
                usuario_id=usuario_id,
                categoria_id=categoria_id,
                titulo=titulo,
                monto=monto,
                descripcion=descripcion,
            )
            nuevo_gasto.save()
            return redirect('home')  # Redirige a la vista que desees

        context = {
            'categorias': categorias,
        }
        return render(request, 'nuevoGasto.html', context)
    else:
        return redirect('login')

