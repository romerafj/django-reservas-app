from django.contrib import admin
from django.urls import path, include
from . import views  # Importa las vistas del directorio actual ('cn')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reservas/', include('reservas.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.login_view, name='login'),
]