# Generated by Django 5.2.1 on 2025-05-18 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0003_configuracionrecordatorio'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='email_notificacion',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email de Notificación'),
        ),
    ]
