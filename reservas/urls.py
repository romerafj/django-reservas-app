from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_reservas, name='lista_reservas'),
    path('crear/', views.crear_reserva, name='crear_reserva'),
    path('<int:reserva_id>/', views.detalle_reserva, name='detalle_reserva'),
    path('modificar/<int:reserva_id>/', views.modificar_reserva, name='modificar_reserva'),
    path('eliminar/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('configuracion-recordatorios/', views.configuracion_recordatorios, name='configuracion_recordatorios'),
]