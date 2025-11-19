from django import forms
from .models import Reserva, Sala

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
        
        # Que sea un dropdown
        self.fields['nombre_sala'].choices = opciones

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        
        if not rut:
            raise forms.ValidationError("El rut es obligatorio.")
        
        if len(rut) < 9 or len(rut) > 10:
            raise forms.ValidationError("El rut debe tener entre 9 y 10 caracteres contando el guión.")
        
        return rut