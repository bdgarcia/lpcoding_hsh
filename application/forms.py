from django import forms
from modelos.models import Residencia
from django.core.exceptions import NON_FIELD_ERRORS


class ResidenciaForm(forms.ModelForm):
    class Meta:
        model=Residencia
        fields=('nombre', 'ubicacion', 'descripcion', 'precio', 'monto_minimo_subasta', 'foto',)
        labels = {                                                  #Hace un override de los labels.
            'ubicacion': 'Ubicación',
            'descripcion': 'Descripción',
            'monto_minimo_subasta': 'Monto mínimo de subasta',
        }

        
class TestForm(forms.Form):
    monto = forms.FloatField()
        



            
