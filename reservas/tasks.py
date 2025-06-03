# reservas/tasks.py
from django.core.mail import send_mail
from django.conf import settings
import datetime
from reservas.models import Reserva
from django_rq import job  # Asegúrate de que esta importación siga aquí si la añadiste antes

# Si decoraste la función con @job antes, elimínalo si vas a usar solo el cron del sistema operativo.

def enviar_recordatorios():
    now = datetime.datetime.now(datetime.timezone.utc).astimezone()
    asunto = 'Recordatorio de vuelo'
    mensaje = 'Este es un recordatorio de tu próximo vuelo.'
    reservas = Reserva.objects.exclude(email_notificacion__isnull=True).exclude(email_notificacion__exact='')
    lista_de_correos = [reserva.email_notificacion for reserva in reservas]
    if lista_de_correos:
        send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, lista_de_correos)
        print(f"Intentando enviar recordatorios a las reservas a las {now.strftime('%H:%M %Z%z')}")
    else:
        print("No se encontraron reservas con correo electrónico de notificación para enviar recordatorios.")
    print(f"Función enviar_recordatorios ejecutada a las {now.strftime('%H:%M %Z%z')}")