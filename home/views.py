from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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

        if request.method == 'POST':
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

def nuevo_presupuesto(request):
    if request.method == 'POST' and 'usuario_id' in request.session:
        usuario = request.user  # Obtener el usuario actual
        
        # Obtener los datos del formulario
        categoria_id = request.POST.get('categoria')
        limite_presupuesto = request.POST.get('limite_presupuesto')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        # Crear un nuevo presupuesto
        presupuesto = Presupuestos(
            usuario_id=request.session['usuario_id'],  # Asignar el usuario actual
            categoria_id=categoria_id,
            limite_presupuesto=limite_presupuesto,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        presupuesto.save()
        
        return redirect('nuevo-gasto')  # Cambia esta ruta según tu necesidad

    # Obtener todas las categorías para el formulario
    categorias = Categorias.objects.all()
    return render(request, 'nuevoPresupuesto.html', {'categorias': categorias})

def nueva_categoria(request):
    if request.method == 'POST' and 'usuario_id' in request.session:
        usuario = request.user  # Obtener el usuario actual
        
        # Obtener los datos del formulario
        nombre_categoria = request.POST.get('nombre_categoria')
        descripcion = request.POST.get('descripcion')
        
        # Crear una nueva categoría
        categoria = Categorias(
            usuario_id = request.session['usuario_id'],
            nombre_categoria=nombre_categoria,
            descripcion=descripcion
        )
        categoria.save()
        
        return redirect('nuevo-gasto')  # Cambia esta ruta según tu necesidad

    return render(request, 'nuevaCategoria.html')

def eliminar_categoria(request):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        categorias = Categorias.objects.filter(usuario_id=usuario_id)
        
        if request.method == 'POST':
            categoria_id = request.POST.get('categoria')
            categoria = get_object_or_404(Categorias, id_categoria=categoria_id, usuario_id=usuario_id)
            categoria.delete()
            return redirect('home')

    return render(request, 'eliminarCategoria.html', {'categorias': categorias})

def eliminar_presupuesto(request):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        presupuestos = Presupuestos.objects.filter(usuario_id=usuario_id)
        
        if request.method == 'POST':
            presupuesto_id = request.POST.get('presupuesto')
            presupuesto = get_object_or_404(Presupuestos, id_presupuesto=presupuesto_id, usuario_id=usuario_id)
            presupuesto.delete()
            return redirect('home')
    return render(request, 'eliminarPresupuesto.html', {'presupuestos': presupuestos})