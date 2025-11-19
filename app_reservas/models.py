from django.db import models
from datetime import datetime, timedelta

# Create your models here.

#modelo para las salas
class Sala(models.Model):
    nombre = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    disponible = models.BooleanField(default=True)

#modelo para las reservas
class Reserva(models.Model):
    rut = models.CharField(max_length=12)
    nombre_sala = models.CharField(max_length=50)
    fecha_reserva = models.DateField(auto_now_add=True) #con el auto_now_add se guarda la fecha automaticamente
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def calcular_hora_fin(self):
        # Convertir hora_inicio a datetime, sumar 2 horas
        hora_inicio_dt = datetime.combine(datetime.today(), self.hora_inicio)
        hora_fin_dt = hora_inicio_dt + timedelta(hours=2)
        return hora_fin_dt.time()

#esta funcion guarda la hora fin en la reserva en la bd
    def save(self):
        # Calcular hora_fin automáticamente antes de guardar
        self.hora_fin = self.calcular_hora_fin()
        super().save()

