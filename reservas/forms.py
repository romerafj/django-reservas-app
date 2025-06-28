from django import forms
from .models import Reserva

from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['activa', 'origen', 'destino', 'fecha_vuelo', 'fecha_emision',
                  'fecha_deposito', 'fecha_pago_total', 'compania', 'pnr',
                  'notas', 'deposito_realizado', 'emitida', 'pagado_total',
                  'email_notificacion', 'forma_pago', 'importe_deposito',
                  'fecha_cancelacion_plazas', 'observaciones_cancelacion_plazas',
                  'fecha_cancelacion_total', 'importe_pago_total', 'fecha_nombres',
                  'tipo_cliente', 'nombre_agencia']
        widgets = {
            'fecha_vuelo': forms.DateInput(attrs={'type': 'date'}),
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_deposito': forms.DateInput(attrs={'type': 'date'}),
            'fecha_pago_total': forms.DateInput(attrs={'type': 'date'}),
            'fecha_cancelacion_plazas': forms.DateInput(attrs={'type': 'date'}),
            'fecha_cancelacion_total': forms.DateInput(attrs={'type': 'date'}),
            'fecha_nombres': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_cliente = cleaned_data.get('tipo_cliente')
        nombre_agencia = cleaned_data.get('nombre_agencia')

        if tipo_cliente in ['AD_HOC', 'CATALOGO'] and not nombre_agencia:
            self.add_error('nombre_agencia', 'El nombre de la agencia es obligatorio para este tipo de cliente.')

        return cleaned_data
    
from django import forms
from .models import ConfiguracionRecordatorio

class ConfiguracionRecordatorioForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionRecordatorio
        fields = ['dias_antes_deposito', 'dias_antes_pago_total', 'dias_antes_emision']
        labels = {
            'dias_antes_deposito': 'Avisar con (días) antes del Depósito',
            'dias_antes_pago_total': 'Avisar con (días) antes del Pago Total',
            'dias_antes_emision': 'Avisar con (días) antes de la Emisión',
        }
        widgets = {
            'dias_antes_deposito': forms.NumberInput(attrs={'min': 0}),
            'dias_antes_pago_total': forms.NumberInput(attrs={'min': 0}),
            'dias_antes_emision': forms.NumberInput(attrs={'min': 0}),
        }