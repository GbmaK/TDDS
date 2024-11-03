from django.urls import path
from .views import home_view, nuevo_gasto, nuevo_presupuesto , nueva_categoria, eliminar_categoria, eliminar_presupuesto

urlpatterns = [
    path('', home_view, name='home'),  
    path('nuevo-gasto', nuevo_gasto, name='nuevo-gasto'),
    path('nuevoPresupuesto/', nuevo_presupuesto, name='nuevoPresupuesto'),
    path('nuevaCategoria/', nueva_categoria, name='nuevaCategoria'),
    path('eliminar-categoria/', eliminar_categoria, name='eliminar-categoria'),
    path('eliminar-presupuesto/', eliminar_presupuesto, name='eliminar-presupuesto'),
]