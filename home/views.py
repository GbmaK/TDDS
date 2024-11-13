from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from .models import Gastos, Categorias, Presupuestos, Notificaciones

def home_view(request):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']

        # Obtener los gastos, categorías y presupuestos del usuario
        gastos = Gastos.objects.filter(usuario_id=usuario_id)
        categorias = Categorias.objects.filter(usuario_id=usuario_id)
        presupuestos = Presupuestos.objects.filter(usuario_id=usuario_id)
        notificaciones = Notificaciones.objects.filter(usuario_id=usuario_id)

        # Calcular el presupuesto restante por cada presupuesto
        presupuestos_data = []
        for presupuesto in presupuestos:
            # Obtener la suma de los gastos para la categoría asociada al presupuesto
            total_gastos = Gastos.objects.filter(
                categoria_id=presupuesto.categoria.id_categoria, usuario_id=usuario_id
            ).aggregate(Sum('monto'))['monto__sum'] or 0

            # Calcular el presupuesto restante
            presupuesto_restante = presupuesto.limite_presupuesto - total_gastos

            # Agregar los datos calculados a la lista
            presupuestos_data.append({
                'categoria': presupuesto.categoria,
                'limite_presupuesto': presupuesto.limite_presupuesto,
                'gasto_total': total_gastos,
                'presupuesto_restante': presupuesto_restante
            })

        context = {
            'gastos': gastos,
            'categorias': categorias,
            'presupuestos': presupuestos_data,  # Usar los datos calculados
            'notificaciones': notificaciones,
        }

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
            monto = Decimal(request.POST.get('monto'))
            descripcion = request.POST.get('descripcion')

            # Obtener el presupuesto de la categoría seleccionada
            presupuesto = Presupuestos.objects.filter(categoria_id=categoria_id, usuario_id=usuario_id).first()

            # Verificar si hay un presupuesto para la categoría
            if presupuesto:
                # Calcular la suma de los gastos actuales para esa categoría
                total_gastos = Gastos.objects.filter(categoria_id=categoria_id, usuario_id=usuario_id).aggregate(Sum('monto'))['monto__sum'] or 0

                # Verificar si el nuevo gasto excedería el presupuesto
                if total_gastos + monto > presupuesto.limite_presupuesto:
                    # Bloquear el gasto y mostrar mensaje de advertencia
                    messages.error(request, f"No se puede agregar el gasto. El presupuesto para esta categoría es de ${presupuesto.limite_presupuesto} y ya has gastado ${total_gastos}.")
                else:
                    # Registrar el nuevo gasto
                    nuevo_gasto = Gastos(
                        usuario_id=usuario_id,
                        categoria_id=categoria_id,
                        titulo=titulo,
                        monto=monto,
                        descripcion=descripcion,
                    )
                    nuevo_gasto.save()
                    messages.success(request, "Gasto agregado exitosamente.")
                    return redirect('home')
            else:
                messages.error(request, "No hay un presupuesto definido para esta categoría.")

        context = {
            'categorias': categorias,
        }
        return render(request, 'nuevoGasto.html', context)
    else:
        return redirect('login')

def nuevo_presupuesto(request):
    if request.method == 'POST' and 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']  # Obtener el ID del usuario actual
        
        # Obtener los datos del formulario
        categoria_id = request.POST.get('categoria')
        limite_presupuesto = request.POST.get('limite_presupuesto')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        # Verificar si ya existe un presupuesto para esta categoría y usuario
        existing_presupuesto = Presupuestos.objects.filter(
            categoria_id=categoria_id, usuario_id=usuario_id
        ).first()

        if existing_presupuesto:
            # Si ya existe un presupuesto, mostrar mensaje de error
            messages.error(request, "Ya tienes un presupuesto asignado a esta categoría.")
            return redirect('nuevoPresupuesto')  # O redirigir a donde necesites

        # Crear un nuevo presupuesto si no existe uno para esta categoría
        presupuesto = Presupuestos(
            usuario_id=usuario_id,  # Asignar el usuario actual
            categoria_id=categoria_id,
            limite_presupuesto=limite_presupuesto,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        presupuesto.save()

        # Mensaje de éxito y redirección
        messages.success(request, "Presupuesto creado exitosamente.")
        return redirect('home')  # O redirigir a la página que desees

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
            
            if categoria_id:
                # Obtener la categoría por 'id_categoria' y usuario
                categoria = get_object_or_404(Categorias, id_categoria=categoria_id, usuario_id=usuario_id)
                categoria.delete() 
                return redirect('home')
            else:
                # Si no se especifica una categoría, mostrar un mensaje de error
                error_message = "No se seleccionó una categoría para eliminar."
                return render(request, 'eliminarCategoria.html', {'categorias': categorias, 'error_message': error_message})
    
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

def eliminar_gasto(request, gasto_id):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        # Obtener el gasto a eliminar
        gasto = get_object_or_404(Gastos, id_gasto=gasto_id, usuario_id=usuario_id)

        # Eliminar el gasto
        gasto.delete()
        
        # Mensaje de éxito
        messages.success(request, "Gasto eliminado exitosamente.")
        
        # Redirigir al home
        return redirect('home')
    else:
        return redirect('login')
    
def historial_gastos(request):
    # Obtener el usuario de la sesión
    usuario_id = request.session.get('usuario_id')
    
    # Filtros iniciales
    gastos = Gastos.objects.filter(usuario_id=usuario_id)

    # Leer los filtros de la solicitud GET
    titulo = request.GET.get('titulo')
    categoria_id = request.GET.get('categoria')
    fecha = request.GET.get('fecha')
    monto = request.GET.get('monto')
    
    # Aplicar los filtros a la consulta
    if titulo:
        gastos = gastos.filter(titulo__icontains=titulo)
    if categoria_id:
        gastos = gastos.filter(categoria_id=categoria_id)
    if fecha:
        gastos = gastos.filter(fecha__date=fecha)  # Suponiendo que `fecha` es tipo Date
    if monto:
        try:
            gastos = gastos.filter(monto=Decimal(monto))
        except Decimal.InvalidOperation:
            pass  # Ignorar si el monto no es un número válido

    # Obtener todas las categorías para el filtro de categoría
    categorias = Categorias.objects.filter(usuario_id=usuario_id)

    context = {
        'gastos': gastos,
        'categorias': categorias,
    }
    
    return render(request, 'historialGastos.html', context)