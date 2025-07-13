import os
import django
import datetime
import pytz
from django.conf import settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cn.settings")
    django.setup()

    from reservas.models import Reserva
    from django.core.mail import send_mail
    from django.utils import timezone
    from reservas.models import ConfiguracionRecordatorio

    # Especifica la zona horaria de España
    spain_tz = pytz.timezone('Europe/Madrid')
    now_spain = timezone.localtime(timezone.now(), spain_tz)
    today = now_spain.date()

    # --- Obtener la URL base del entorno o usar la de Render directamente ---
    base_url = os.environ.get('SITE_URL') or os.environ.get('RENDER_EXTERNAL_HOSTNAME')

    if not base_url:
        if os.environ.get('RENDER'):
            base_url = 'mis-reservas-django.onrender.com'
        else:
            base_url = '127.0.0.1:8000'

    if not base_url.startswith('http'):
        base_url = f'https://{base_url}'

    print(f"Ejecutando script de envío de correos (hora España): {now_spain.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    print(f"URL base utilizada: {base_url}")

    try:
        configuracion = ConfiguracionRecordatorio.objects.first()
        if configuracion:
            reservas_a_notificar = []
            asunto = 'Recordatorio de vuelo'
            copia_oculta_email = 'romerafj@gmail.com'

            # --- CAMBIO AQUÍ: Filtrar solo por reservas activas (activa=True) ---
            # También mantenemos los filtros para email_notificacion no nulo/vacío
            active_reservas = Reserva.objects.filter(activa=True).exclude(
                email_notificacion__isnull=True
            ).exclude(
                email_notificacion__exact=''
            )

            for reserva in active_reservas: # Iteramos sobre las reservas activas
                # Notificación para fecha_deposito
                if reserva.fecha_deposito:
                    dias_deposito = (reserva.fecha_deposito - today).days
                    if -configuracion.dias_antes_deposito <= dias_deposito <= configuracion.dias_antes_deposito:
                        mensaje = f'Recordatorio: El depósito del vuelo con PNR {reserva.pnr} con origen en {reserva.origen} y destino a {reserva.destino} vence en {dias_deposito} días.'
                        if dias_deposito < 0:
                            mensaje = f'Recordatorio: El depósito del vuelo con PNR {reserva.pnr} con origen en {reserva.origen} y destino a {reserva.destino} venció hace {abs(dias_deposito)} días.'
                        
                        mensaje += f' Puedes modificar tu reserva aquí: {base_url}/reservas/modificar/{reserva.id}/'
                        reservas_a_notificar.append((reserva.email_notificacion, mensaje))
                
                # Notificación para fecha_pago_total
                if reserva.fecha_pago_total:
                    dias_pago_total = (reserva.fecha_pago_total - today).days
                    if -configuracion.dias_antes_pago_total <= dias_pago_total <= configuracion.dias_antes_pago_total:
                        mensaje = f'Recordatorio: El pago total del vuelo con PNR {reserva.pnr} con origen en {reserva.origen} y destino a {reserva.destino} vence en {dias_pago_total} días.'
                        if dias_pago_total < 0:
                            mensaje = f'Recordatorio: El pago total del vuelo con PNR {reserva.pnr} con origen en {reserva.origen} y destino a {reserva.destino} venció hace {abs(dias_pago_total)} días.'
                        
                        mensaje += f' Puedes modificar tu reserva aquí: {base_url}/reservas/modificar/{reserva.id}/'
                        reservas_a_notificar.append((reserva.email_notificacion, mensaje))
                
                # Notificación para fecha_emision
                if reserva.fecha_emision:
                    dias_emision = (reserva.fecha_emision - today).days
                    if -configuracion.dias_antes_emision <= dias_emision <= configuracion.dias_antes_emision:
                        mensaje = f'Recordatorio: La fecha de emisión del vuelo con PNR {reserva.pnr} con origen en {reserva.origen} y destino a {reserva.destino} es en {dias_emision} días.'
                        if dias_emision < 0:
                            mensaje = f'Recordatorio: La fecha de emisión del vuelo con PNR {reserva.pnr} con origen en {reserva.origen} y destino a {reserva.destino} venció hace {abs(dias_emision)} días.'
                        
                        mensaje += f' Puedes modificar tu reserva aquí: {base_url}/reservas/modificar/{reserva.id}/'
                        reservas_a_notificar.append((reserva.email_notificacion, mensaje))

            correos_enviados = set()
            for email, mensaje in reservas_a_notificar:
                if email not in correos_enviados:
                    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [email, copia_oculta_email], fail_silently=False)
                    print(f"Enviando recordatorio a {email} (copia a {copia_oculta_email}): {mensaje}")
                    correos_enviados.add(email)

            if correos_enviados:
                print(f"Se enviaron recordatorios a {len(correos_enviados)} direcciones de correo electrónico.")
            else:
                print("No hay reservas activas para notificar hoy según la configuración.") # Mensaje actualizado

        else:
            print("No se encontró la configuración del recordatorio.")

    except Exception as e:
        print(f"Ocurrió un error al enviar los correos: {e}")

    print("Script de envío de correos finalizado.")