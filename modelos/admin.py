from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Usuario


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = ['email', 'username']


admin.site.register(Usuario, CustomUserAdmin)
from .models import Residencia
admin.site.register(Residencia)
from .models import Subasta
admin.site.register(Subasta)
from .models import Puja
admin.site.register(Puja)
from .models import Alquila
admin.site.register(Alquila)