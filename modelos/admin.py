from django.contrib import admin

# Register your models here.

from .models import Residencia
admin.site.register(Residencia)
from .models import Usuario
admin.site.register(Usuario)
from .models import Subasta
admin.site.register(Subasta)
from .models import Puja
admin.site.register(Puja)
from .models import Alquila
admin.site.register(Alquila)