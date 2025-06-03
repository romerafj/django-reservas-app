from django.db import models
from django.contrib.auth.models import User


class Reserva(models.Model):
    FORMA_PAGO_CHOICES = [
        ('MD', 'Metálico/Datafono'),
        ('TRANSF', 'Transferencia'),
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
    fecha_deposito = models.DateField()
    fecha_pago_total = models.DateField()
    compania = models.CharField(max_length=100)
    localizador = models.CharField(max_length=20, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    deposito_realizado = models.BooleanField(default=False)
    emitida = models.BooleanField(default=False)
    pagado_total = models.BooleanField(default=False)
    email_notificacion = models.EmailField(blank=True, null=True, verbose_name="Email de Notificación")

    forma_pago = models.CharField(max_length=10, choices=FORMA_PAGO_CHOICES, blank=True, null=True, verbose_name="Forma de Pago")
    importe_deposito = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Importe Depósito")
    fecha_cancelacion_plazas = models.DateField(blank=True, null=True, verbose_name="Fecha Cancelación Plazas")
    observaciones_cancelacion_plazas = models.TextField(blank=True, null=True, verbose_name="Observaciones Cancelación Plazas")
    fecha_cancelacion_total = models.DateField(blank=True, null=True, verbose_name="Fecha Cancelación Total")
    importe_pago_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Importe Pago Total")
    fecha_nombres = models.DateField(blank=True, null=True, verbose_name="Fecha Nombres")
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE_CHOICES, verbose_name="Tipo de Cliente")
    nombre_agencia = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre de Agencia")

    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reservas_creadas', null=True, blank=True)
    usuario_modificacion = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reservas_modificadas', null=True, blank=True)

    def __str__(self):
        return f"Reserva a {self.destino} ({self.fecha_vuelo.strftime('%d/%m/%Y %H:%M')})"

    class Meta:
        ordering = ['fecha_vuelo'] # Ordenar por fecha de vuelo por defecto

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