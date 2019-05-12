from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Usuario
        fields = ('nombre', 'apellido', 'fecha_nacimiento', 'tarjeta_credito', 'username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido', 'fecha_nacimiento', 'tarjeta_credito', 'username', 'email')