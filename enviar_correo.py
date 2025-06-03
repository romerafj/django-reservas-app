import os
import django
import datetime
import pytz

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cn.settings")
    django.setup()

    from reservas.models import Reserva
    from django.core.mail import send_mail
    from django.conf import settings
    from django.utils import timezone
    from reservas.models import ConfiguracionRecordatorio

    # Especifica la zona horaria de España
    spain_tz = pytz.timezone('Europe/Madrid')
    now_spain = timezone.localtime(timezone.now(), spain_tz)
    today = now_spain.date()
    base_url = 'http://127.0.0.1:8000'  # URL base de tu aplicación

    print(f"Ejecutando script de envío de correos (hora España): {now_spain.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")

    try:
        configuracion = ConfiguracionRecordatorio.objects.first()
        if configuracion:
            reservas_a_notificar = []
            asunto = 'Recordatorio de vuelo'

            for reserva in Reserva.objects.exclude(email_notificacion__isnull=True).exclude(email_notificacion__exact=''):
                if reserva.fecha_deposito:
                    dias_deposito = (reserva.fecha_deposito - today).days
                    if 0 <= dias_deposito <= configuracion.dias_antes_deposito:
                        mensaje = f'Recordatorio: El depósito del vuelo con localizador {reserva.localizador} con origen en {reserva.origen} y destino a {reserva.destino} vence en {dias_deposito} días. Puedes modificar tu reserva aquí: {base_url}/reservas/modificar/{reserva.id}/'
                        reservas_a_notificar.append((reserva.email_notificacion, mensaje))
                if reserva.fecha_pago_total:
                    dias_pago_total = (reserva.fecha_pago_total - today).days
                    if 0 <= dias_pago_total <= configuracion.dias_antes_pago_total:
                        mensaje = f'Recordatorio: El pago total del vuelo con localizador {reserva.localizador} con origen en {reserva.origen} y destino a {reserva.destino} vence en {dias_pago_total} días. Puedes modificar tu reserva aquí: {base_url}/reservas/modificar/{reserva.id}/'
                        reservas_a_notificar.append((reserva.email_notificacion, mensaje))
                if reserva.fecha_emision:
                    dias_emision = (reserva.fecha_emision - today).days
                    if 0 <= dias_emision <= configuracion.dias_antes_emision:
                        mensaje = f'Recordatorio: La fecha de emisión del vuelo con localizador {reserva.localizador} con origen en {reserva.origen} y destino a {reserva.destino} es en {dias_emision} días. Puedes modificar tu reserva aquí: {base_url}/reservas/modificar/{reserva.id}/'
                        reservas_a_notificar.append((reserva.email_notificacion, mensaje))

            correos_enviados = set()
            for email, mensaje in reservas_a_notificar:
                if email not in correos_enviados:
                    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [email])
                    print(f"Enviando recordatorio a {email}: {mensaje}")
                    correos_enviados.add(email)

            if correos_enviados:
                print(f"Se enviaron recordatorios a {len(correos_enviados)} direcciones de correo electrónico.")
            else:
                print("No hay reservas para notificar hoy según la configuración.")

        else:
            print("No se encontró la configuración del recordatorio.")

    except Exception as e:
        print(f"Ocurrió un error al enviar los correos: {e}")

    print("Script de envío de correos finalizado.")