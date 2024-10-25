from django.urls import path
from .views import home_view, nuevo_gasto

urlpatterns = [
    path('', home_view, name='home'),  
    path('nuevo-gasto', nuevo_gasto, name='nuevo-gasto')
]