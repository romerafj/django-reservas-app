from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva, ConfiguracionRecordatorio
from .forms import ReservaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import ReservaForm, ConfiguracionRecordatorioForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_reservas')  # Asegúrate de que esta URL exista en reservas/urls.py
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Credenciales inválidas'})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

@login_required
def lista_reservas(request):
    reservas = Reserva.objects.all().order_by('-fecha_vuelo')
    estado_filtro = request.GET.get('estado')

    if estado_filtro == 'activa':
        reservas = reservas.filter(activa=True)
    elif estado_filtro == 'desactivada':
        reservas = reservas.filter(activa=False)

    return render(request, 'reservas/lista_reservas.html', {'reservas': reservas})
@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario_creacion = request.user
            reserva.usuario_modificacion = request.user
            reserva.save()
            return redirect('lista_reservas')
    else:
        form = ReservaForm()
    return render(request, 'reservas/crear_reserva.html', {'form': form})

@login_required
def detalle_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    return render(request, 'reservas/detalle_reserva.html', {'reserva': reserva})

@login_required
def modificar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    print(f"Fecha de vuelo de la reserva: {reserva.fecha_vuelo}")  # Añade esta línea AQUÍ
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario_modificacion = request.user
            reserva.save()
            return redirect('detalle_reserva', reserva_id=reserva.id)
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'reservas/modificar_reserva.html', {'form': form, 'reserva': reserva})

@login_required
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    if request.method == 'POST':
        reserva.delete()
        return redirect('lista_reservas')
    return render(request, 'reservas/eliminar_reserva.html', {'reserva': reserva})

@login_required
def configuracion_recordatorios(request):
    try:
        configuracion = ConfiguracionRecordatorio.objects.get()
    except ConfiguracionRecordatorio.DoesNotExist:
        configuracion = ConfiguracionRecordatorio.objects.create()

    if request.method == 'POST':
        form = ConfiguracionRecordatorioForm(request.POST, instance=configuracion)
        if form.is_valid():
            form.save()
            return redirect('configuracion_recordatorios')  # Redirige a la misma página con mensaje de éxito
    else:
        form = ConfiguracionRecordatorioForm(instance=configuracion)

    return render(request, 'reservas/configuracion_recordatorios.html', {'form': form})