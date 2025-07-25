# Generated by Django 5.2.1 on 2025-06-27 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0005_reserva_fecha_cancelacion_plazas_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reserva',
            options={'ordering': ['fecha_vuelo'], 'verbose_name': 'Reserva', 'verbose_name_plural': 'Reservas'},
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='localizador',
        ),
        migrations.AddField(
            model_name='reserva',
            name='fecha_limite_reduccion_plazas',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Límite Reducción Plazas'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='numero_plazas',
            field=models.PositiveIntegerField(default=1, verbose_name='Número de Plazas'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='pnr',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='PNR'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='primer_pago',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Primer Pago'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='fecha_deposito',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Depósito'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='forma_pago',
            field=models.CharField(blank=True, choices=[('MD', 'Metálico/Datafono'), ('TRANSF', 'Transferencia'), ('EMD', 'EMD')], max_length=10, null=True, verbose_name='Forma de Pago'),
        ),
    ]
