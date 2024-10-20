from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_categoria = models.CharField(max_length=60)
    descripcion = models.TextField()

class Gasto(models.Model):
    id_gasto = models.AutoField(primary_key=True)  # Esto corresponde a la columna 'id' en la tabla
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User
    categoria_id = models.IntegerField()  # O ForeignKey a Categoria si lo tienes
    titulo = models.CharField(max_length=255)  # Nuevo campo para el título
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    class Meta:
        db_table = 'Gastos'

class Presupuesto(models.Model):
    id_presupuesto = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User
    categoria_id = models.IntegerField()  # O ForeignKey a Categoria si lo tienes
    limite_presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    class Meta:
        db_table = 'Presupuestos'

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    umbral = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_notificacion = models.CharField(max_length=60)
    activo = models.BooleanField(default=True)

class HistorialGasto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    gasto = models.ForeignKey(Gasto, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
