from modelos.models import (Usuario)
u = Usuario(username='admin')
u.set_password('123')
u.is_superuser = True
u.is_staff = True
u.nombre = ("Test")
u.apellido = ("Test")
u.email = ("Test@gmail.com")
u.fecha_nacimiento = ("1997-12-12")
u.creditos = (2)
u.type = ("admin")
u.save()

u = Usuario(username='osvaldo.mantecovich@gmail.com')
u.set_password('123')
u.is_superuser = True
u.is_staff = True
u.nombre = ("Osvaldo")
u.apellido = ("Mantecovich")
u.email = ('osvaldo.mantecovich@gmail.com')
u.fecha_nacimiento = ("1987-03-23")
u.creditos = (2)
u.type = ("admin")
u.save()
us = Usuario(username='sebastia.villena@gmail.com')
us.set_password('123')
us.is_superuser = False
us.is_staff = False
us.is_active = True
us.nombre = ("Sebastian")
us.apellido = ("Villena")
us.email = ("sebastia.villena@gmail.com")
us.fecha_nacimiento = ("1997-12-13")
us.numero_tarjeta = ("4830806605707486")
us.vencimiento_tarjeta=("01/25")
us.codigo_tarjeta=(902)
us.creditos = (2)
us.type = ("premium")
us.save()
use = Usuario(username='rociobrindesi@gmail.com')
use.set_password('123')
use.is_superuser = False
use.is_staff = False
use.nombre = ("Roro")
use.apellido = ("Brindesi")
use.email = ("rociobrindesi@gmail.com")
use.fecha_nacimiento = ("1998-6-27")
use.numero_tarjeta = (5574842721834331)
use.vencimiento_tarjeta=("02/22")
use.codigo_tarjeta=(582)
use.creditos = (2)
use.type = ("comun")
use.save()
user = Usuario(username='brunodg91@gmail.com')
user.set_password('123')
user.is_superuser = False
user.is_staff = False
user.nombre = ("Bruno")
user.apellido = ("Garcia")
user.email = ("brunodg91@gmail.com")
user.fecha_nacimiento = ("1991-01-27")
user.numero_tarjeta = (4004442535586012)
user.vencimiento_tarjeta=("02/24")
user.codigo_tarjeta=(643)
user.creditos = (2)
user.type = ("comun")
user.save()
uuser = Usuario(username='michi@gmail.com')
uuser.set_password('123')
uuser.is_superuser = False
uuser.is_staff = False
uuser.nombre = ("michi")
uuser.apellido = ("michifus")
uuser.email = ("michi@gmail.com")
uuser.fecha_nacimiento = ("2000-01-27")
uuser.numero_tarjeta = (4647825126886283)
uuser.vencimiento_tarjeta=("11/24")
uuser.codigo_tarjeta=(670)
uuser.creditos = (2)
uuser.type = ("premium")
uuser.save()
from modelos.models import Variables_sistema
p = Variables_sistema()
p.precio_usuario_comun = 1000
p.precio_usuario_premium = 5000
p.save()
from modelos.models import Residencia
r = Residencia()
r.nombre = "Casa de mauri"
r.ubicacion = "City Bell, calle 471"
r.descripcion = "Es grande, calculo que algun baño tiene, tiene gatos aunque no los vi, la mitad de los patys tienen queso y el resto no, hay mayonesa vegana"
r.precio = 0
r.monto_minimo_subasta = 1200.99
r.foto = "Casa_de_murito-La_faculta.jpg"
r.save()

r = Residencia()
r.nombre = "Casa de Ro"
r.ubicacion = "Villa Elisa, calle 420"
r.descripcion = "Tiene un baño, dos dormitorios, cocina grande con comedor integrado, sala de estar, una perrita llamada ruya. Se preparan muy buenas picsas"
r.precio = 0
r.monto_minimo_subasta = 1200.99
r.foto = "Casa_de_ro.jpg"
r.save()

r = Residencia()
r.nombre = "Casa de Sebas"
r.ubicacion = "La Plata calle 12"
r.descripcion = "Dos dormitorios, dos patios pequeños, estar comedor juntos, dos michis hermosos y cariñosos"
r.precio = 0
r.monto_minimo_subasta = 1200.99
r.foto = "Casa_de_sebas.jpg"
r.save()

r = Residencia()
r.nombre = "Casa de Bruno calle 58"
r.ubicacion = "La Plata"
r.descripcion = "Tiene un michi muy cariñoso y uno muy timido, cocina amplia y baño"
r.precio = 0
r.monto_minimo_subasta = 1200.99
r.foto = "Casa_de_bruno.jpg"
r.save()


from modelos.models import (Subasta, Alquila, Residencia)
from application.cerrar_subasta import cerrarSubasta
import datetime

def cerrarSubastasDeLaSemana():
    subastas = list(Subasta.objects.filter(semana_alquila=lunesEn6Meses))
    print("Cerrando subastas de esta semana")
    for subasta in subastas:
        cerrarSubasta(subasta)
    print(len(subastas), "subasta/s cerradas")

def evaluarSubasta(res, lunesActual, miercolesActual, lunesEn6Meses, today):
    import datetime
    from modelos.models import (Subasta, Alquila, Residencia)
    from application.cerrar_subasta import cerrarSubasta
    print("evaluando: ", res.codigo, res.nombre)
    # 0=lunes, 2=miercoles
    if (0 <= (datetime.date.today().weekday() )<= 2):
        if not Subasta.objects.filter(semana_alquila=lunesEn6Meses, codigo_residencia=res).exists() and not Alquila.objects.filter(fecha=lunesEn6Meses, codigo_residencia=res).exists():
            print("Creando: ", res.codigo)
            s = Subasta()
            s.codigo_residencia = res
            s.monto_actual = res.monto_minimo_subasta
            s.monto_inicial = res.monto_minimo_subasta
            s.fecha_inicio = lunesActual
            s.fecha_fin = miercolesActual
            s.semana_alquila = lunesEn6Meses
            s.save()

today = datetime.date.today()
lunesActual = (today - datetime.timedelta(days=today.weekday()))
miercolesActual = (today - datetime.timedelta(days=today.weekday()-2))
lunesEn6Meses = (lunesActual + datetime.timedelta(6*365/12))

residencias = Residencia.objects.filter(borrado_logico=False)
for res in residencias:
    evaluarSubasta(res, lunesActual, miercolesActual, lunesEn6Meses, today)


if 3 <= datetime.date.today().weekday():
    cerrarSubastasDeLaSemana()