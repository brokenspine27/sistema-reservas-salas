from django import forms
from .models import Reserva, Sala
from datetime import datetime, timedelta

class ReservaForm(forms.Form):
    rut = forms.CharField(max_length=10)
    nombre_sala = forms.ChoiceField(choices=[])
    hora_inicio = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        initial='09:00'
    )

    def __init__(self):
        super().__init__()
        
        # Filtrar salas disponibles
        salas_disponibles = Sala.objects.filter(disponible=True)
        opciones = [(sala.nombre, sala.nombre) for sala in salas_disponibles]
        
        # Que se puedan elegir las salas. Aqui se le pasa el dato a las opciones
        self.fields['nombre_sala'].choices = opciones


#validacion para el rut
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        
        if not rut:
            raise forms.ValidationError("El rut es obligatorio.")
        
        if len(rut) < 9 or len(rut) > 10:
            raise forms.ValidationError("El rut debe tener entre 9 y 10 caracteres contando el guión.")
        
        return rut
    
#nuevo metodo para evitar superposición de reservas

    def clean(self):
        cleaned_data = super().clean()
        nombre_sala = cleaned_data.get('nombre_sala')
        hora_inicio = cleaned_data.get('hora_inicio')
        
        if nombre_sala and hora_inicio:
            from .models import Reserva
            
            #calculo de la hora
            
            hora_inicio_dt = datetime.combine(datetime.today(), hora_inicio)
            hora_fin_calculada = (hora_inicio_dt + timedelta(hours=2)).time()
            
            #buscar superposicion
            
            reservas_solapadas = Reserva.objects.filter(
                nombre_sala=nombre_sala,
                fecha_reserva=datetime.today()
            ).filter(
                #casos donde se solapan
                # Caso 1: Nueva reserva empieza DENTRO de una existente
                hora_inicio__lte=hora_inicio,
                hora_fin__gt=hora_inicio
            ) | Reserva.objects.filter(
                nombre_sala=nombre_sala,
                fecha_reserva=datetime.today()
            ).filter(
                # Caso 2: Nueva reserva termina DENTRO de una existente
                hora_inicio__lt=hora_fin_calculada,
                hora_fin__gte=hora_fin_calculada
            ) | Reserva.objects.filter(
                nombre_sala=nombre_sala,
                fecha_reserva=datetime.today()
            ).filter(
                # Caso 3: Nueva reserva CONTIENE una existente
                hora_inicio__gte=hora_inicio,
                hora_fin__lte=hora_fin_calculada
            )
            
            if reservas_solapadas.exists():
                raise forms.ValidationError(
                    f"La sala {nombre_sala} ya tiene reservas en el horario seleccionado. "
                    f"Horario no disponible: {hora_inicio} - {hora_fin_calculada}"
                )
        
        return cleaned_data