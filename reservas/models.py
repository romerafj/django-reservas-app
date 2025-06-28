from django.db import models
from django.contrib.auth.models import User


class Reserva(models.Model):
    FORMA_PAGO_CHOICES = [
        ('MD', 'Metálico/Datafono'),
        ('TRANSF', 'Transferencia'),
        ('EMD', 'EMD'), # ¡AÑADIDO! Nueva opción para forma de pago
    ]

    TIPO_CLIENTE_CHOICES = [
        ('AD_HOC', 'Ad Hoc'),
        ('CATALOGO', 'Catálogo'),
        ('PLAZA_A_PLAZA', 'Plaza a Plaza'),
    ]

    activa = models.BooleanField(default=True)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha_reserva = models.DateTimeField(auto_now_add=True)  # Se guarda automáticamente al crear la reserva
    fecha_vuelo = models.DateField()
    fecha_emision = models.DateField()
    # fecha_deposito ahora no es obligatoria
    fecha_deposito = models.DateField(blank=True, null=True, verbose_name="Fecha Depósito")
    fecha_pago_total = models.DateField()
    compania = models.CharField(max_length=100)
    # localizador cambiado a PNR
    pnr = models.CharField(max_length=20, blank=True, null=True, verbose_name="PNR")
    notas = models.TextField(blank=True, null=True)
    deposito_realizado = models.BooleanField(default=False)
    emitida = models.BooleanField(default=False)
    pagado_total = models.BooleanField(default=False)
    email_notificacion = models.EmailField(blank=True, null=True, verbose_name="Email de Notificación")

    forma_pago = models.CharField(max_length=10, choices=FORMA_PAGO_CHOICES, blank=True, null=True, verbose_name="Forma de Pago")
    importe_deposito = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Importe Depósito")
    # Nuevo campo: primer_pago (no obligatorio)
    primer_pago = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Primer Pago")
    fecha_cancelacion_plazas = models.DateField(blank=True, null=True, verbose_name="Fecha Cancelación Plazas")
    observaciones_cancelacion_plazas = models.TextField(blank=True, null=True, verbose_name="Observaciones Cancelación Plazas")
    fecha_cancelacion_total = models.DateField(blank=True, null=True, verbose_name="Fecha Cancelación Total")
    importe_pago_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Importe Pago Total")
    fecha_nombres = models.DateField(blank=True, null=True, verbose_name="Fecha Nombres")
    # Nuevo campo: fecha_limite_reduccion_plazas
    fecha_limite_reduccion_plazas = models.DateField(blank=True, null=True, verbose_name="Fecha Límite Reducción Plazas")
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE_CHOICES, verbose_name="Tipo de Cliente")
    nombre_agencia = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre de Agencia")
    # Nuevo campo: numero_plazas
    numero_plazas = models.PositiveIntegerField(default=1, verbose_name="Número de Plazas")

    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reservas_creadas', null=True, blank=True)
    usuario_modificacion = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reservas_modificadas', null=True, blank=True)

    def __str__(self):
        # Asegúrate de que 'fecha_vuelo' sea un objeto datetime si quieres formatear con %H:%M
        # Si es un DateField, quitar %H:%M. Lo mantendré como DateField por ahora.
        return f"Reserva a {self.destino} ({self.fecha_vuelo.strftime('%d/%m/%Y')}) - PNR: {self.pnr or 'N/A'}"

    class Meta:
        ordering = ['fecha_vuelo']
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

class ConfiguracionRecordatorio(models.Model):
    dias_antes_deposito = models.IntegerField(default=2)
    dias_antes_pago_total = models.IntegerField(default=2)
    dias_antes_emision = models.IntegerField(default=2)

    def __str__(self):
        return "Configuración de Recordatorios"
        
class ConfiguracionRecordatorio(models.Model):
    dias_antes_deposito = models.IntegerField(default=1)
    dias_antes_pago_total = models.IntegerField(default=2)
    dias_antes_emision = models.IntegerField(default=3)

    def __str__(self):
        return "Configuración de Recordatorios"

    class Meta:
        verbose_name = "Configuración de Recordatorio"
        verbose_name_plural = "Configuraciones de Recordatorios"