from modelos.models import (Usuario)
u = Usuario(username='admin')
u.set_password('123')
u.is_superuser = True
u.is_staff = True
u.nombre = ("nombre")
u.apellido = ("apellido")
u.email = ("email@email.com")
u.fecha_nacimiento = ("1997-12-12")
u.tarjeta_credito = ("123123123")
u.creditos = (2)
u.type = ("admin")
u.save()
