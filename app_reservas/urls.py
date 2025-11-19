from django.urls import path, include
from . import views

#rutas para las vistas, vista inicial y vista para crear reservas
urlpatterns = [
    path('', views.lista_salas, name='home'),
    path('reservar/', views.crear_reserva, name='crear_reserva')
]

#faltaria una ruta para ver las salas en detalle.