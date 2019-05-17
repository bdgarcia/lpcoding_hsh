from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import Usuario


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("username", "type",)
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('username', 'type', 'email', 'fecha_nacimiento', 'creditos', 'nombre', 'apellido', 'is_superuser', 'is_staff', 'is_active')}),
        )
    add_fieldsets = ((None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'type', 'email', 'fecha_nacimiento', 'creditos', 'is_superuser', 'is_staff', 'is_active')}
            ),
        )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Usuario, CustomUserAdmin)
from .models import Residencia
admin.site.register(Residencia)
from .models import Subasta
admin.site.register(Subasta)
from .models import Puja
admin.site.register(Puja)
from .models import Alquila
admin.site.register(Alquila)