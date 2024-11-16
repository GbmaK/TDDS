from django.urls import path
from .views import home_view, nuevo_gasto, nuevo_presupuesto , nueva_categoria, eliminar_categoria, eliminar_presupuesto, eliminar_gasto, historial_gastos, exportar_historial_a_excel, exportar_historial_a_pdf

urlpatterns = [
    path('', home_view, name='home'),  
    path('nuevo-gasto', nuevo_gasto, name='nuevo-gasto'),
    path('nuevoPresupuesto/', nuevo_presupuesto, name='nuevoPresupuesto'),
    path('nuevaCategoria/', nueva_categoria, name='nuevaCategoria'),
    path('eliminar-categoria/', eliminar_categoria, name='eliminar-categoria'),
    path('eliminar-presupuesto/', eliminar_presupuesto, name='eliminar-presupuesto'),
    path('eliminar-gasto/<int:gasto_id>/', eliminar_gasto, name='eliminar-gasto'),
    path('historialGastos/', historial_gastos, name='historial-gastos'),
    path('exportar_excel/', exportar_historial_a_excel, name='exportar-historial-a-excel'),
    path('exportar_pdf/', exportar_historial_a_pdf, name='exportar-historial-a-pdf'),
]