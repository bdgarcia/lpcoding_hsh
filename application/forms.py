from django import forms
from modelos.models import Residencia, Usuario, Variables_sistema
from django.core.exceptions import NON_FIELD_ERRORS
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.forms import (PasswordResetForm, SetPasswordForm)



class ResidenciaForm(forms.ModelForm):
    class Meta:
        model=Residencia
        fields=('nombre', 'ubicacion', 'descripcion', 'precio', 'monto_minimo_subasta', 'foto',)
        labels = {                                                 
            'ubicacion': 'Ubicación',
            'descripcion': 'Descripción',
            'monto_minimo_subasta': 'Monto mínimo de subasta',
        }

        
class TestForm(forms.Form):
    monto = forms.FloatField()

class UsuarioForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput() ,label="Repita la contraseña")
    class Meta:
        model=Usuario
        fields=('email', 'nombre', 'apellido', 'fecha_nacimiento', 'numero_tarjeta', 'vencimiento_tarjeta','codigo_tarjeta', 'password')
        labels= {
            "fecha_nacimiento": "Fecha de nacimiento",
            "numero_tarjeta": "Número de tarjeta de crédito",
            "vencimiento_tarjeta": "Fecha de vencimiento de la tarjeta",
            "codigo_tarjeta": "Código de seguridad de la tarjeta"
        }
        widgets={
            "password": forms.PasswordInput(),
            "fecha_nacimiento":forms.SelectDateWidget(years=range(date.today().year, 1920, -1))
        }
        error_messages = {
            'numero_tarjeta': {
                'invalid': "Ingrese un número de tarjeta válido."
            },
            'vencimiento_tarjeta':{
                'date_passed': "La fecha de vencimiento de la tarjeta ya ha expirado."
            },
            'codigo_tarjeta': {
                'invalid': "Ingrese un código de seguridad válido"
            },
            'email': {
                'unique': "Ya existe un usuario con este email."
            }
        }

    def clean(self):
        cleaned_data = super(UsuarioForm, self).clean()
        contraseña= cleaned_data["password"]
        confirmacion= cleaned_data["confirm_password"]
        if contraseña!=confirmacion:
            raise forms.ValidationError("Las contraseñas no coinciden.")


    def clean_fecha_nacimiento(self): 
        fecha_n= self.cleaned_data["fecha_nacimiento"]
        today=date.today()
        age = today.year - fecha_n.year - ((today.month, today.day) < (fecha_n.month, fecha_n.day))
        if (age<18):
            raise forms.ValidationError("Debe ser mayor de 18 años.")
        return fecha_n
    
    def super_clean(self):
        super().clean()

class Variables_sistemaForm(forms.ModelForm):
    class Meta:
        model=Variables_sistema
        fields=("precio_usuario_comun", "precio_usuario_premium")

    def clean_precio_usuario_comun(self):
        precio= self.cleaned_data["precio_usuario_comun"]
        if precio < 0:
            raise forms.ValidationError("Valor invalido.")
        return precio

    def clean_precio_usuario_premium(self):
        precio= self.cleaned_data["precio_usuario_premium"]
        if precio < 0:
            raise forms.ValidationError("Valor invalido.")
        return precio


    

class UsuarioFormOtro(forms.ModelForm):
    class Meta:
        model=Usuario
        fields=( 'nombre', 'apellido', 'numero_tarjeta', 'vencimiento_tarjeta','codigo_tarjeta')
        labels= {
            "numero_tarjeta": "Número de tarjeta de crédito",
            "vencimiento_tarjeta": "Fecha de vencimiento de la tarjeta",
            "codigo_tarjeta": "Código de seguridad de la tarjeta"
        }

        error_messages = {
            'numero_tarjeta': {
                'invalid': "Ingrese un número de tarjeta válido."
            },
            'codigo_tarjeta': {
                'invalid': "Ingrese un código de seguridad válido"
            }
        }

        

class UsuarioFormContraseña(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput() ,label="Repita la contraseña")
    class Meta:
        model=Usuario
        fields=('password',)
        widgets={
            "password": forms.PasswordInput(),
        }
        

    def clean(self):
        cleaned_data = super(UsuarioFormContraseña, self).clean()
        contraseña= cleaned_data["password"]
        confirmacion= cleaned_data["confirm_password"]
        if contraseña!=confirmacion:
            raise forms.ValidationError("Las contraseñas no coinciden.")


class AdminForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput() ,label="Repita la contraseña")
    class Meta:
        model=Usuario
        fields=('email', 'nombre', 'apellido', 'fecha_nacimiento', 'password')
        labels= {
            "fecha_nacimiento": "Fecha de nacimiento",
        }
        widgets={
            "password": forms.PasswordInput(),
            "fecha_nacimiento":forms.SelectDateWidget(years=range(date.today().year, 1920, -1))
        }
        error_messages = {
            'email': {
                'unique': "Ya existe un usuario con este email."
            }
        }
    def clean(self):
        cleaned_data = super(AdminForm, self).clean()
        contraseña= cleaned_data["password"]
        confirmacion= cleaned_data["confirm_password"]
        if contraseña!=confirmacion:
            raise forms.ValidationError("Las contraseñas no coinciden.")


    def clean_fecha_nacimiento(self): 
        fecha_n= self.cleaned_data["fecha_nacimiento"]
        today=date.today()
        age = today.year - fecha_n.year - ((today.month, today.day) < (fecha_n.month, fecha_n.day))
        if (age<18):
            raise forms.ValidationError("Debe ser mayor de 18 años.")
        return fecha_n
    
    def super_clean(self):
        super().clean()







class MySetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("¡Las contraseñas no coinciden!"),
    }
    new_password1 = forms.CharField(
        label=("Contraseña nueva"),
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password2 = forms.CharField(
        label=("Repita la contraseña"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(MySetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
           

    