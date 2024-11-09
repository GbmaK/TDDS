# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Categorias(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    nombre_categoria = models.CharField(max_length=60)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categorias'

class Gastos(models.Model):
    id_gasto = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, blank=True, null=True)  # Cambiado a CASCADE
    titulo = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'gastos'


class Historialgastos(models.Model):
    id_historial = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    gasto = models.ForeignKey(Gastos, models.DO_NOTHING, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'historialgastos'


class HomeCategoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=60)
    descripcion = models.TextField()
    usuario_id = models.IntegerField()

    class Meta:
        db_table = 'home_categoria'


class Notificaciones(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, blank=True, null=True)  # Cambiado a CASCADE
    umbral = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_notificacion = models.CharField(max_length=60, blank=True, null=True)
    activo = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'notificaciones'


class Presupuestos(models.Model):
    id_presupuesto = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, blank=True, null=True)  # Cambiado a CASCADE
    limite_presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'presupuestos'

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    contraseña = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'usuarios'