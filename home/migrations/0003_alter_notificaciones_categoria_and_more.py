# Generated by Django 5.1.1 on 2024-11-17 00:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_gastos_categoria_alter_gastos_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificaciones',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.categorias'),
        ),
        migrations.AlterField(
            model_name='presupuestos',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.categorias'),
        ),
    ]
