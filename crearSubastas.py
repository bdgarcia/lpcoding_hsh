from modelos.models import (Subasta, Alquila, Residencia)
from application.cerrar_subasta import cerrarSubasta
import datetime

def cerrarSubastasDeLaSemana():
    subastas = list(Subasta.objects.filter(semana_alquila=lunesEn6Meses))
    print("Cerrando subastas de esta semana")
    for subasta in subastas:
        cerrarSubasta(subasta)
    print(len(subastas), "subasta/s cerradas")

def evaluarSubasta(res):
    print("evaluando: ", res.codigo, res.nombre)
    # 0=lunes, 2=miercoles
    if 0 <= datetime.date.today().weekday() <= 7:
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
    evaluarSubasta(res)


if 8 <= datetime.date.today().weekday():
    cerrarSubastasDeLaSemana()

