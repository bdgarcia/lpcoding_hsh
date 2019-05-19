from django import forms
from modelos.models import Residencia
from modelos.models import Puja


class ResidenciaForm(forms.ModelForm):
    class Meta:
        model=Residencia
        fields=('nombre', 'ubicacion', 'descripcion', 'precio', 'monto_minimo_subasta', 'foto',)
        labels = {                                                  #Hace un override de los labels.
            'ubicacion': 'Ubicación',
            'descripcion': 'Descripción',
            'monto_minimo_subasta': 'Monto mínimo de subasta',
        }
        
class PujaForm(forms.ModelForm):
    class Meta:
        model = Puja
        monto = forms.FloatField(label="Monto" )