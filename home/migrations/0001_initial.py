# Generated by Django 5.1.1 on 2024-10-22 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_categoria', models.CharField(max_length=60)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'categorias',
            },
        ),
        migrations.CreateModel(
            name='HomeCategoria',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre_categoria', models.CharField(max_length=60)),
                ('descripcion', models.TextField()),
                ('usuario_id', models.IntegerField()),
            ],
            options={
                'db_table': 'home_categoria',
            },
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('contraseña', models.CharField(max_length=255)),
                ('fecha_creacion', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'usuarios',
            },
        ),
        migrations.CreateModel(
            name='Gastos',
            fields=[
                ('id_gasto', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.categorias')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.usuarios')),
            ],
            options={
                'db_table': 'gastos',
            },
        ),
        migrations.CreateModel(
            name='Presupuestos',
            fields=[
                ('id_presupuesto', models.AutoField(primary_key=True, serialize=False)),
                ('limite_presupuesto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_inicio', models.DateTimeField(blank=True, null=True)),
                ('fecha_fin', models.DateTimeField(blank=True, null=True)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.categorias')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.usuarios')),
            ],
            options={
                'db_table': 'presupuestos',
            },
        ),
        migrations.CreateModel(
            name='Notificaciones',
            fields=[
                ('id_notificacion', models.AutoField(primary_key=True, serialize=False)),
                ('umbral', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo_notificacion', models.CharField(blank=True, max_length=60, null=True)),
                ('activo', models.IntegerField(blank=True, null=True)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.categorias')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.usuarios')),
            ],
            options={
                'db_table': 'notificaciones',
            },
        ),
        migrations.CreateModel(
            name='Historialgastos',
            fields=[
                ('id_historial', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('gasto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.gastos')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.usuarios')),
            ],
            options={
                'db_table': 'historialgastos',
            },
        ),
        migrations.AddField(
            model_name='categorias',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.usuarios'),
        ),
    ]