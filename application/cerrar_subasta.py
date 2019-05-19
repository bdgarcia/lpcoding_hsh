from modelos.models import (Puja, Alquila)

def cerrarSubasta(subasta):
    pujas = list(Puja.objects.filter(codigo_subasta=subasta))
    # ordena las pujas de mayor a menor por el monto de las mismas
    pujas.sort(key=lambda x: x.monto, reverse=True)
    se_alquilo = False
    for puja in pujas:
        if puja.usuario.creditos > 0:
            user = puja.usuario
            user.creditos = user.creditos-1
            user.save()
            a = Alquila()
            a.codigo_residencia = puja.codigo_subasta.codigo_residencia
            a.fecha = puja.codigo_subasta.semana_alquila
            a.precio = puja.monto
            a.email_usuario = puja.usuario
            a.save()
            se_alquilo = True
            print("El usuario: ", user.email, "gano la subasta de: ", a.codigo_residencia.nombre)
        if se_alquilo:
            break
    if not se_alquilo:
        if len(pujas) > 0:
            print("Los usuarios no poseen suficientes creditos, nadie gano la subasta")
        else:
            print("Nadie pujo por la residencia: ", subasta.codigo_residencia.nombre)
    subasta.delete()
