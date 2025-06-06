# Generated by Django 5.2.1 on 2025-05-18 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0002_alter_reserva_fecha_vuelo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionRecordatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dias_antes_deposito', models.IntegerField(default=1)),
                ('dias_antes_pago_total', models.IntegerField(default=2)),
                ('dias_antes_emision', models.IntegerField(default=3)),
            ],
            options={
                'verbose_name': 'Configuración de Recordatorio',
                'verbose_name_plural': 'Configuraciones de Recordatorios',
            },
        ),
    ]
