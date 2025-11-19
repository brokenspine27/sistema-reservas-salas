# Register your models here.
from django.contrib import admin
from .models import Sala, Reserva

class SalaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'capacidad', 'disponible']
    list_filter = ['disponible']
    search_fields = ['nombre']

class ReservaAdmin(admin.ModelAdmin):
    list_display = ['rut', 'nombre_sala', 'fecha_reserva', 'hora_inicio', 'hora_fin']
    list_filter = ['fecha_reserva', 'nombre_sala']
    search_fields = ['rut', 'nombre_sala']

# registro de los modelos en el admin
admin.site.register(Sala, SalaAdmin)
admin.site.register(Reserva, ReservaAdmin)