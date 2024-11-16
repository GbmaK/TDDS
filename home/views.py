from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from .models import Gastos, Categorias, Presupuestos, Notificaciones, Historialgastos
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas
from datetime import datetime
from django.template.defaultfilters import date

def home_view(request):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        fecha_seleccionada = request.GET.get('fecha')  # Obtener la fecha seleccionada desde la solicitud

        # Filtrar los gastos, categorías y presupuestos del usuario
        gastos = Gastos.objects.filter(usuario_id=usuario_id)
        if fecha_seleccionada:
            gastos = gastos.filter(fecha__date=fecha_seleccionada)  # Filtrar los gastos por la fecha seleccionada

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
            'fecha_seleccionada': fecha_seleccionada,  # Enviar la fecha seleccionada al template
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
            return redirect('nuevoPresupuesto')

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
        return redirect('home')

    # Obtener solo las categorías asociadas al usuario actual para el formulario
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        categorias = Categorias.objects.filter(usuario_id=usuario_id)
    else:
        categorias = Categorias.objects.none()

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
    usuario_id = request.session.get('usuario_id')  # Obtener el ID del usuario de la sesión
    gastos = Gastos.objects.filter(usuario_id=usuario_id)  # Filtrar los gastos del usuario

    # Leer los filtros de la solicitud GET
    titulo = request.GET.get('titulo')
    categoria_id = request.GET.get('categoria')
    fecha = request.GET.get('fecha')
    monto = request.GET.get('monto')

    # Aplicar los filtros a la consulta de gastos
    if titulo:
        gastos = gastos.filter(titulo__icontains=titulo)
    if categoria_id:
        gastos = gastos.filter(categoria_id=categoria_id)
    if fecha:
        gastos = gastos.filter(fecha__date=fecha) 
    if monto:
        try:
            gastos = gastos.filter(monto=Decimal(monto))
        except Decimal.InvalidOperation:
            messages.error(request, "Monto no válido.")

    # Obtener todas las categorías para el filtro de categoría
    categorias = Categorias.objects.filter(usuario_id=usuario_id)

    # Retornar los gastos filtrados al template
    context = {
        'gastos': gastos,
        'categorias': categorias,
    }

    return render(request, 'historialGastos.html', context)


def exportar_historial_a_excel(request):
    usuario_id = request.session.get('usuario_id')
    gastos = Gastos.objects.filter(usuario_id=usuario_id)

    # Filtrar si hay parámetros de búsqueda
    titulo = request.GET.get('titulo', '')
    categoria_id = request.GET.get('categoria', '')
    fecha = request.GET.get('fecha', '')

    if titulo:
        gastos = gastos.filter(titulo__icontains=titulo)
    if categoria_id:
        gastos = gastos.filter(categoria_id=categoria_id)
    if fecha:
        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
            gastos = gastos.filter(fecha__date=fecha)
        except ValueError:
            pass  # Si el formato de fecha es incorrecto, se ignora el filtro

    # Verificar si hay datos para exportar
    if not gastos.exists():
        messages.error(request, "No hay datos para exportar.")
        return redirect('historial_gastos')

    # Crear el archivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = 'Historial de Gastos'

    # Escribir los encabezados
    ws.append(['Título', 'Categoría', 'Monto', 'Fecha', 'Descripción'])

    # Escribir los datos de los gastos
    for gasto in gastos:
        # Usar el filtro date para formatear la fecha como en el HTML
        if gasto.fecha:
            formatted_date = date(gasto.fecha, 'b. d, Y, P')  # Formato: Nov. 15, 2024, 7:22 a.m
        else:
            formatted_date = None

        ws.append([gasto.titulo, gasto.categoria.nombre_categoria, gasto.monto, formatted_date, gasto.descripcion])

    # Crear la respuesta HTTP para descargar el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=historial_gastos.xlsx'
    wb.save(response)
    return response

def exportar_historial_a_pdf(request):
    usuario_id = request.session.get('usuario_id')
    gastos = Gastos.objects.filter(usuario_id=usuario_id)

    # Filtrar si hay parámetros de búsqueda
    titulo = request.GET.get('titulo', '')
    categoria_id = request.GET.get('categoria', '')
    fecha = request.GET.get('fecha', '')

    if titulo:
        gastos = gastos.filter(titulo__icontains=titulo)
    if categoria_id:
        gastos = gastos.filter(categoria_id=categoria_id)
    if fecha:
        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
            gastos = gastos.filter(fecha__date=fecha)
        except ValueError:
            pass  # Si el formato de fecha es incorrecto, se ignora el filtro

    # Verificar si hay datos para exportar
    if not gastos.exists():
        messages.error(request, "No hay datos para exportar.")
        return redirect('historial_gastos')

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="historial_gastos.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Crear la tabla con los encabezados
    data = [['Título', 'Categoría', 'Monto', 'Fecha', 'Descripción']]  # Encabezados

    # Agregar cada gasto a la tabla
    for gasto in gastos:
        # Formato de fecha
        if gasto.fecha:
            formatted_date = gasto.fecha.strftime('%b. %d, %Y, %I:%M %p')  # Nov. 15, 2024, 7:22 a.m
        else:
            formatted_date = ''

        data.append([gasto.titulo, gasto.categoria.nombre_categoria, gasto.monto, formatted_date, gasto.descripcion])

    # Crear la tabla
    table = Table(data)

    # Estilo de la tabla
    style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Encabezado blanco
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación central
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),  # Fondo azul para encabezados
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Líneas de la tabla
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente estándar
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de la fuente
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espacio inferior en encabezados
        ('TOPPADDING', (0, 1), (-1, -1), 10),  # Espacio superior en datos
    ])
    table.setStyle(style)

    # Agregar la tabla a los elementos
    elements.append(table)

    # Construir el documento PDF
    doc.build(elements)

    return response