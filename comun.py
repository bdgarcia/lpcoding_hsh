from modelos.models import (Usuario)
from date import datetime

us = Usuario(username='sebastia.villena@gmail.com')
us.set_password('123')
us.is_superuser = False
us.is_staff = False
us.is_active = True
us.nombre = ("Sebastian")
us.apellido = ("Villena")
us.email = ("sebastia.villena@gmail.com")
us.fecha_nacimiento = ("1997-13-12")
us.numero_tarjeta = ("4830806605707486")
print("ok")
us.vencimiento_tarjeta(datetime.datetime(2025, 1, 1))
us.codigo_tarjeta(902)
us.creditos = (2)
us.type = ("premium")
us.save()