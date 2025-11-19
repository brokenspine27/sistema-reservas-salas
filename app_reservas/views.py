from django.shortcuts import render, redirect
from .models import Sala, Reserva
from .forms import ReservaForm
from datetime import datetime, timedelta

def lista_salas(request):
    #variables necesarias 
    salas = Sala.objects.all()
    hoy = datetime.now().date()
    hora_actual = datetime.now().time()
    
    # Para cada sala, verificar si tiene reservas activas hoy
    for sala in salas:
        reservas_hoy = Reserva.objects.filter(
            nombre_sala=sala.nombre,
            fecha_reserva=hoy
        )
        
        # Marcar si tiene reservas en el momento actual
        sala.reservas_hoy = reservas_hoy
        sala.ocupada_ahora = False

        #verificar reservas activas
        for reserva in reservas_hoy:
            fecha_hora_actual = datetime.combine(hoy, hora_actual)
            hora_inicio_dt = datetime.combine(hoy, reserva.hora_inicio)
            hora_fin_dt = datetime.combine(hoy, reserva.hora_fin)

#si la hora actual esta entrmedio de las horas de la reserva, la sala esta ocupada
            if hora_inicio_dt <= fecha_hora_actual <= hora_fin_dt:
                sala.ocupada_ahora = True
                break

    
    context = {
        'salas': salas,
        'titulo': 'Salas de Estudio Disponibles'
    }
    
    return render(request, 'lista_salas.html', context)

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm()
        # Llenar el form manualmente
        form.data = request.POST
        form.is_bound = True
        
        if form.is_valid():
            # Calcular hora_fin con timedelta que suma dos horas de diferencia
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_inicio_dt = datetime.combine(datetime.today(), hora_inicio)
            hora_fin_dt = hora_inicio_dt + timedelta(hours=2)
            
            # Crear y guardar la reserva manualmente
            reserva = Reserva(
                rut=form.cleaned_data['rut'],
                nombre_sala=form.cleaned_data['nombre_sala'],
                hora_inicio=hora_inicio,
                hora_fin=hora_fin_dt.time()
            )
            reserva.save()
            
            return redirect('home')
    else:
        form = ReservaForm()
    
    context = {
        'form': form,
        'titulo': 'Reservar Sala de Estudio'
    }
    
    return render(request, 'reservar.html', context)