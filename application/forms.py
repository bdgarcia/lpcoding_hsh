from django import forms
from modelos.models import Residencia, Usuario
from django.core.exceptions import NON_FIELD_ERRORS
from datetime import date, timedelta


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

class UsuarioForm(forms.ModelForm):
    class Meta:
        model=Usuario
        fields=('username', 'password', 'nombre', 'apellido', 'email', 'fecha_nacimiento')#, 'tarjeta_credito')
        labels= {
            "fecha_nacimiento": "Fecha de nacimiento:"
           #"tarjeta_credito": "Tarjeta de credito:"
        }
        widgets={
            "password": forms.PasswordInput(),
            "fecha_nacimiento":forms.SelectDateWidget(years=range(date.today().year, 1920, -1))
        }



    def clear_fecha_nacimiento(self): 
        limite=date.today()-timedelta(years=18)#time.strftime(%d, %m, %Y)
        fecha = self.cleaned_data['fecha_nacimiento']
        if fecha<limite:
            messages.error(request, "Fecha de nacimiento menos a 18 años")
            raise forms.ValidationError("Fecha de nacimiento menor a 18 años")
