import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from modelos.models import Residencia
from modelos.models import Subasta
from modelos.models import Puja
from modelos.models import Usuario
from modelos.models import Alquila
from modelos.models import HotSale
from modelos.models import Variables_sistema
from django.contrib.auth import login
from creditcards import types

from django.contrib.auth import update_session_auth_hash
from .forms import ResidenciaForm, UsuarioForm, Variables_sistemaForm, UsuarioFormOtro, UsuarioFormContraseña
from datetime import date, timedelta, datetime, time
# Create your views here.

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 6
    return d + timedelta(days_ahead)

def calcularFecha():
    today = date.today()
    lunesActual = (today - timedelta(days=today.weekday()))
    lunesEn6Meses = (lunesActual + timedelta(6 * 365 / 12))
    return lunesEn6Meses

def allmondays(fecha, hasta):
    if type(fecha) == str:
        d = datetime.strptime(fecha, '%Y-%m-%d')
    else:
        d = datetime.combine(fecha, time())
    d = d + timedelta(days=-1)
    d = next_weekday(d, 1)
    if type(hasta) == str:
        end = datetime.strptime(hasta, '%Y-%m-%d')
    else:
        end = datetime.combine(hasta, time())
    aux = []
    while d <= end:
        aux.append(d.date())
        d = d + timedelta(days = 7)
    return aux


def index(request):
    allHotsales = HotSale.objects.filter()
    hotsale_list = []
    hotsale_aux = []
    hotsale_dates = []
    for hotsale in allHotsales:
        if hotsale.codigo_residencia not in hotsale_list:
            hotsale_list.append(hotsale.codigo_residencia)
            hotsale_aux.append(hotsale.codigo_residencia.codigo)
            hotsale_dates.append(hotsale.fecha)

    residencias = Residencia.objects.filter(borrado_logico=False)
    subastas = Subasta.objects.all()
    criteria = None
    parametro = None
    if request.method == 'GET': # If the form is submitted
        if request.GET.get('parametro'):
            criteria = request.GET.get('criteria')
            parametro = request.GET.get('parametro')
            if criteria == "nombre":
                residencias = residencias.filter(nombre__icontains=parametro)
            if criteria == "ubicacion":
                residencias = residencias.filter(ubicacion__icontains=parametro)

        if request.GET.get('enSubasta'):
            codigos_subasta = []
            for subasta in subastas:
                codigos_subasta.append(subasta.codigo_residencia.codigo)
            residencias = residencias.filter(codigo__in=codigos_subasta)

        if request.GET.get('fecha') or request.GET.get('hasta'):
            lunesEn6Meses = datetime.combine(calcularFecha(), time())
            if request.GET.get('fecha'):
                fecha_desde = request.GET.get('fecha')
            else:
                fecha_desde = date.today()

            if request.GET.get('hasta'):
                fecha_hasta = request.GET.get('hasta')
            else:
                fecha_hasta = lunesEn6Meses

            if type(fecha_desde) == str:
                desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
            else:
                desde = fecha_desde

            if type(fecha_hasta) == str:
                hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
            else:
                hasta = fecha_hasta

            if desde < lunesEn6Meses:
                fecha_busqueda_normal = lunesEn6Meses
            else:
                fecha_busqueda_normal = desde

            resultado = []
            if fecha_busqueda_normal < hasta:
                todosLosLunes = allmondays(fecha_busqueda_normal, hasta)
                for residencia in residencias:
                    for unLunes in todosLosLunes:
                        alquileres = Alquila.objects.filter(codigo_residencia=residencia)
                        isRented = alquileres.filter(fecha=unLunes)
                        if (not isRented.exists()):
                            if residencia not in resultado:
                                resultado.append(residencia)

            if desde < lunesEn6Meses:
                fecha_busqueda_hotsale = desde
            else:
                fecha_busqueda_hotsale = lunesEn6Meses

            if fecha_busqueda_hotsale < datetime.combine(calcularFecha(), time()):
                todosLosLunes = allmondays(fecha_busqueda_hotsale, hasta)
                for hotsale in allHotsales:
                    for unLunes in todosLosLunes:
                        if unLunes in hotsale_dates:
                            if hotsale.codigo_residencia not in resultado:
                                resultado.append(hotsale.codigo_residencia)

            residencias = resultado

    primer_lunes = calcularFecha()
    fecha_busqueda = primer_lunes.strftime('%Y-%m-%d')
    if request.GET.get('fecha'):
        fecha_desde = request.GET.get('fecha')
    else:
        fecha_desde = None

    if request.GET.get('hasta'):
        fecha_hasta = request.GET.get('hasta')
    else:
        fecha_hasta = None
    subastaOn = None
    if request.GET.get('enSubasta'):
        subastaOn = 'on'

    hotsale = None
    if allHotsales:
        hotsale = 'true'

    hotsale_list = []
    for hotsale in allHotsales:
        if hotsale.codigo_residencia not in hotsale_list:
            hotsale_list.append(hotsale.codigo_residencia)

    return render(request, "index.html", {"residencias": residencias, "subastas": subastas, "comienzo_busqueda": fecha_busqueda , "criteria": criteria, "parametro": parametro, "desde": fecha_desde, "hasta": fecha_hasta, "subastaOn": subastaOn, "hotsale": hotsale, "hotsales": allHotsales, "hotsale_list": hotsale_list})

def catalogo_hotsales(request):
    subastas = Subasta.objects.all()
    allHotsales = HotSale.objects.filter()
    hotsale_list = []
    hotsale_aux = []
    hotsale_dates = []
    for hotsale in allHotsales:
        if hotsale.codigo_residencia not in hotsale_list:
            hotsale_list.append(hotsale.codigo_residencia)
            hotsale_aux.append(hotsale.codigo_residencia.codigo)
            hotsale_dates.append(hotsale.fecha)

    hotsale_list = []
    hotsale_aux = []
    for hotsale in allHotsales:
        if hotsale.codigo_residencia not in hotsale_list:
            hotsale_list.append(hotsale.codigo_residencia)
            hotsale_aux.append(hotsale.codigo_residencia.codigo)

    residencias = Residencia.objects.filter(borrado_logico=False, codigo__in=hotsale_aux)
    criteria = None
    parametro = None
    if request.method == 'GET': # If the form is submitted
        if request.GET.get('parametro'):
            criteria = request.GET.get('criteria')
            parametro = request.GET.get('parametro')
            if criteria == "nombre":
                residencias = residencias.filter(nombre__icontains=parametro)
            if criteria == "ubicacion":
                residencias = residencias.filter(ubicacion__icontains=parametro)

        if request.GET.get('enSubasta'):
            codigos_subasta = []
            for subasta in subastas:
                codigos_subasta.append(subasta.codigo_residencia.codigo)
            residencias = residencias.filter(codigo__in=codigos_subasta)

        if request.GET.get('fecha') or request.GET.get('hasta'):
            lunesEn6Meses = datetime.combine(calcularFecha(), time())
            if request.GET.get('fecha'):
                fecha_desde = request.GET.get('fecha')
            else:
                fecha_desde = date.today()

            if request.GET.get('hasta'):
                fecha_hasta = request.GET.get('hasta')
            else:
                fecha_hasta = lunesEn6Meses

            if type(fecha_desde) == str:
                desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
            else:
                desde = fecha_desde

            if type(fecha_hasta) == str:
                hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
            else:
                hasta = fecha_hasta

            if desde < lunesEn6Meses:
                fecha_busqueda_normal = lunesEn6Meses
            else:
                fecha_busqueda_normal = desde

            resultado = []
            if fecha_busqueda_normal < hasta:
                todosLosLunes = allmondays(fecha_busqueda_normal, hasta)
                for residencia in residencias:
                    for unLunes in todosLosLunes:
                        alquileres = Alquila.objects.filter(codigo_residencia=residencia)
                        isRented = alquileres.filter(fecha=unLunes)
                        if (not isRented.exists()):
                            if residencia not in resultado:
                                resultado.append(residencia)

            if desde < lunesEn6Meses:
                fecha_busqueda_hotsale = desde
            else:
                fecha_busqueda_hotsale = lunesEn6Meses

            if fecha_busqueda_hotsale < datetime.combine(calcularFecha(), time()):
                todosLosLunes = allmondays(fecha_busqueda_hotsale, hasta)
                for hotsale in allHotsales:
                    for unLunes in todosLosLunes:
                        if unLunes in hotsale_dates:
                            if hotsale.codigo_residencia not in resultado:
                                resultado.append(hotsale.codigo_residencia)

            residencias = resultado

    primer_lunes = calcularFecha()
    fecha_busqueda = primer_lunes.strftime('%Y-%m-%d')
    if request.GET.get('fecha'):
        fecha_desde = request.GET.get('fecha')
    else:
        fecha_desde = None

    if request.GET.get('hasta'):
        fecha_hasta = request.GET.get('hasta')
    else:
        fecha_hasta = None
    subastaOn = None
    if request.GET.get('enSubasta'):
        subastaOn = 'on'

    hotsale = None
    if allHotsales:
        hotsale = 'true'

    hotsale_list = []
    for hotsale in allHotsales:
        if hotsale.codigo_residencia not in hotsale_list:
            hotsale_list.append(hotsale.codigo_residencia)

    return render(request, "index.html", {"residencias": residencias, "subastas": subastas, "comienzo_busqueda": fecha_busqueda , "criteria": criteria, "parametro": parametro, "desde": fecha_desde, "hasta": fecha_hasta, "subastaOn": subastaOn, "hotsale": hotsale, "hotsales": allHotsales, "hotsale_list": hotsale_list})


# Create your views here.
def test(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')

# Formulario alta residencia
def alta_residencia(request):
    if (not request.user.is_authenticated) or request.user.type != "admin":
        return redirect("/")
    else:
        subasta=None
        if request.method == "POST":
            form=ResidenciaForm(request.POST, request.FILES)
            if form.is_valid():
                residencia = form.save()
                residencia.save()
                messages.success(request, 'La residencia fue creada correctamente.')
                return redirect("/detalle_residencia/"+ str(residencia.pk))
        else:
            form=ResidenciaForm
        return (render(request,"alta_residencia.html", {'form':form, 'subasta':subasta}))
    

def alta_usuario(request):
    if request.user.is_authenticated and request.user.type != "admin":
        return redirect("/")
    else:
        try:
            subscripcion = Variables_sistema.objects.get(pk = 1)
            subscripcion = subscripcion.precio_usuario_comun
        except Variables_sistema.DoesNotExist:
            subscripcion = 0
        finally:
            if request.method=="POST":
                form=UsuarioForm(request.POST, request.FILES)
                if form.is_valid():
                    usuario=form.save(commit=False)
                    #Para alta de admins: if usuario.type != admin:
                    usuario.username=usuario.email
                    usuario.type="comun"
                    usuario.set_password(usuario.password)
                    usuario.save()
                    if not request.user.is_authenticated:
                        login(request, usuario)
                    messages.success(request, 'El usuario fue creado correctamente')
                    return redirect("/usuario/"+str(usuario.pk))
            else:
                    form=UsuarioForm
            return (render(request, "alta_usuario.html", {"form":form, "subscripcion": subscripcion}))




# Formulario modificacion/baja de residencia
def mod_residencia(request, pk):
    if (not request.user.is_authenticated) or request.user.type != "admin":
        return redirect("/")
    else:
        residencia = get_object_or_404(Residencia, pk=pk)
        try:
            subasta = Subasta.objects.get(codigo_residencia = residencia.pk)
        except Subasta.DoesNotExist:
            subasta = None
        finally:
            if request.method == "POST" and 'btnModificar' in request.POST:
                form = ResidenciaForm(request.POST, instance=residencia) 
                if form.is_valid():
                    residencia = form.save(commit=False) #por si tengo que modificar datos
                    residencia.save()
                    messages.success(request, 'La residencia fue modificada correctamente.')
                    return redirect("/detalle_residencia/"+ str(residencia.pk))
            elif request.method =="POST" and "btnEliminar" in request.POST:
                form=ResidenciaForm(request.POST, instance=residencia)
                residencia=form.save(commit=False)
                residencia.borrado_logico=True
                residencia.save()
                messages.success(request, 'La residencia fue eliminada correctamente.')
                return redirect('/')
            else:
                form = ResidenciaForm(instance=residencia)
            return (render(request, 'alta_residencia.html', {'form': form, "subasta": subasta}))


def alquilar_residencia(request):
    if (not request.user.is_authenticated) or request.user.type != "premium":
        return redirect("/")
    else:
        residencia = Residencia.objects.get(codigo=request.POST.get('codigo'))
        fecha = request.POST.get('week-picker')
        fecha_inicial = fecha.split()[0].replace("/", "-")
        primer_lunes = calcularFecha()
        fecha_busqueda = primer_lunes.strftime('%Y-%m-%d')
        # setear los dias alquilados para no colorearlos como disponibles en el calendario
        diasAlquilados = []
        semanasAlquiladas = Alquila.objects.filter(codigo_residencia=residencia)
        for semana in semanasAlquiladas:
            elLunes = semana.fecha
            for x in range(0, 7):
                dia = elLunes + timedelta(days=x)
                diasAlquilados.append(str(dia))
        semanaSubasta = Subasta.objects.filter(codigo_residencia=residencia)
        for semSubasta in semanaSubasta:
            elLunes = semSubasta.semana_alquila
            for x in range(0, 7):
                dia = elLunes + timedelta(days=x)
                diasAlquilados.append(str(dia))
    return (render(request, 'alquilar_residencia.html', {'residencia': residencia, "diasAlquilados": diasAlquilados, "comienzo_busqueda": fecha_busqueda, "fecha": fecha_inicial}))

def alquilar_hotsale(request):
    if not request.user.is_authenticated:
        return redirect("/")
    else:
        hotsale = HotSale.objects.get(pk=request.POST.get('codigo'))
        residencia = Residencia.objects.get(codigo=hotsale.codigo_residencia.codigo)
    return (render(request, 'alquilar_hotsale.html', {'residencia': residencia, "hotsale": hotsale}))

def confirmar_alquiler(request):
    if request.method == "POST":
        residencia = Residencia.objects.get(codigo=request.POST.get('codigo'))
        usuario = Usuario.objects.get(email=request.user.email)
        usuario.creditos = usuario.creditos-1
        usuario.save()
        alquiler = Alquila()
        alquiler.codigo_residencia = residencia
        fecha = request.POST.get('week-picker').split()[0].replace("/", "-")
        fecha_inicial = datetime.strptime(fecha, '%Y-%m-%d')
        alquiler.fecha = (fecha_inicial - timedelta(days=fecha_inicial.weekday()))
        alquiler.precio = 0
        alquiler.email_usuario = request.user
        alquiler.save()
        messages.success(request, 'La reserva fue realizada con éxito.')
        return redirect("/")


def confirmar_cancelacion_alquiler(request, pk):
    alquiler=get_object_or_404(Alquila, pk=pk)
    fecha= date.today()
    if (request.user == alquiler.email_usuario) and (not alquiler.cancelado):
        if request.method == "POST":
            if 'btnCancelarAlq' in request.POST:
                #Aca estaria el codigo que retorna la plata al usuario.
                alquiler.cancelado = True
                alquiler.save()
                messages.success(request, 'El alquiler ha sido cancelado correctamente.')
            else:
                messages.success(request, 'El alquiler no ha sido cancelado.')
            return redirect('/usuario/'+str(alquiler.email_usuario.pk))
    else:
        return redirect("/")
    return (render(request, 'confirmar_cancelacion_alquiler.html', {'alquiler':alquiler, "fecha": fecha}))

def confirmar_hotsale(request):
    if request.method == "POST":
        residencia = Residencia.objects.get(codigo=request.POST.get('codigo'))
        hotsale = HotSale.objects.get(pk=request.POST.get('codigo_hotsale'))
        alquiler = Alquila()
        alquiler.codigo_residencia = residencia
        alquiler.fecha = hotsale.fecha
        alquiler.precio = hotsale.precio
        alquiler.email_usuario = request.user
        alquiler.save()
        hotsale.delete()
        messages.success(request, 'La reserva fue realizada con éxito.')
        return redirect("/")

def configurar_tarifas(request):
    if (not request.user.is_authenticated) or request.user.type != "admin":
        return redirect("/")
    else:
        tarifa=get_object_or_404(Variables_sistema, pk=1)
        if request.method == "POST" and 'btnModificar' in request.POST:
            form=Variables_sistemaForm(request.POST, instance=tarifa)
            if form.is_valid():
                tarifa=form.save(commit=False)
                tarifa.save()
                messages.success(request, 'Tarifas guardadas.')
                return redirect("administracion")
        elif request.method == "POST" and 'btnCancelar' in request.POST:
            messages.error(request, "Cambios de tarifas cancelados.")
            return redirect("administracion")
        else:
            form=Variables_sistemaForm(instance=tarifa)
        return (render(request, 'configurar_tarifas.html', {'form': form}))


def get_CC_type(codigo):
    """Retorna la marca de la tarjeta"""
    for tarjeta in types.CC_TYPES:
        if tarjeta[0] == codigo:
            aux=tarjeta[1]
            return aux["title"]
    return "Marca genérica/NA"


def detalle_usuario (request, pk):
    usuario= get_object_or_404(Usuario,pk=pk)
    alquileres = Alquila.objects.filter(email_usuario = pk)
    marca_tarjeta= get_CC_type(types.get_type(usuario.numero_tarjeta))
    vencimiento_cred= usuario.date_joined.date()
    aux= vencimiento_cred.year + 1 + (date.today().year - usuario.date_joined.year)
    aux= vencimiento_cred.replace(year = aux)
    fecha= date.today()
    return (render(request, "detalle_usuario.html", {"usuario": usuario, "alquileres": alquileres, "marca": marca_tarjeta, "vencimiento_creditos":aux, "fecha":fecha}))



# Muestra el listado de usuarios, permitiendo ordenar por el criterio deseado
def listado_usuarios(request):
    if (request.user.is_authenticated and request.user.type == "admin"):
        return redirect("/listado_usuarios/alfabetico_des")
    return redirect("/")


def listado_usuarios_modo(request, modo):
    if modo == "alfabetico_as" or modo == "fregistro_as" or modo == "alfabetico_des" or modo == "fregistro_des":
        if (request.user.is_authenticated and request.user.type == "admin"):
            users = Usuario.objects.all()
            if modo == "alfabetico_des":
                users = sorted(users, key= lambda x: x.username.lower(), reverse = False)
            elif modo == "alfabetico_as":
                users = sorted(users, key= lambda x: x.username.lower(), reverse = True)
            elif modo == "fregistro_as":
                users = sorted(users, key= lambda x: x.date_joined, reverse = True)
            elif modo == "fregistro_des":
                users = sorted(users, key= lambda x: x.date_joined, reverse = False)
            return (render (request, "listado_usuarios.html" , {"users": users}))
    return redirect("/")

def modificar_admin(usuario, usr):
    usuario.nombre = usr.nombre
    usuario.apellido = usr.apellido
    usuario.save()

def modificar_otro(usuario, usr):
    usuario.nombre = usr.nombre
    usuario.apellido = usr.apellido
    usuario.numero_tarjeta = usr.numero_tarjeta
    usuario.vencimiento_tarjeta = usr.vencimiento_tarjeta
    usuario.codigo_tarjeta = usr.codigo_tarjeta
    usuario.save()

def editar_usuario(request, pk):
    if request.user.is_authenticated and (request.user.type == "admin" or request.user.pk == pk):
        usuario= get_object_or_404(Usuario,pk=pk)
        if request.method == "POST":
            if 'btnDescartar' in request.POST:
                messages.success(request, "Los cambios han sido descartados")
                return redirect("/usuario/"+str(pk))
            elif 'btnModificar' in request.POST:
                form = UsuarioFormOtro(request.POST, request.FILES, instance=usuario)
                if form.is_valid():
                    usr= form.save(commit = False)
                    if usuario.type == "admin":
                        modificar_admin(usuario, usr)
                    else:
                        modificar_otro(usuario, usr)
                    messages.success(request, "El usuario ha sido modificado")
                    return redirect("/usuario/"+str(pk))
                else:
                    return (render (request, "modificar_usuario.html", {"form": form,  "usuario": usuario}))
        else:
            form = UsuarioFormOtro(instance=usuario)
            return (render (request, "modificar_usuario.html", {"form": form,  "usuario": usuario}))
    return redirect("/")

def cambiar_contraseña(request, pk):
    if request.user.is_authenticated and request.user.pk == pk:
        usuario= get_object_or_404(Usuario,pk=pk)
        if request.method == "POST":
            if 'btnDescartar' in request.POST:
                form = UsuarioFormContraseña(request.POST, request.FILES, instance=usuario)
                form.password= "a"
                form.confirm_password= "a"
                messages.success(request, "Los cambios han sido descartados")
                return redirect("/usuario/"+str(pk))
            elif 'btnModificar' in request.POST:
                form = UsuarioFormContraseña(request.POST, request.FILES, instance=usuario)
                if form.is_valid():
                    usr = form.save(commit=False)
                    usuario.set_password(usr.password)
                    usuario.save()
                    update_session_auth_hash(request, usuario)  # Important!
                    messages.success(request, "La contraseña ha sido cambiada")
                    return redirect("/usuario/"+str(pk))
                return (render (request, "modificar_contraseña.html", {"form": form,  "usuario": usuario}))
        form = UsuarioFormContraseña(instance=usuario)
        return (render (request, "modificar_contraseña.html", {"form": form,  "usuario": usuario}))
    return redirect("/")





# Redirecciona a la pagina de inicio si no se le pasan parametros a detalle_residencia
def detalle_residencia_solo (request):
    return redirect("index")

# Muestra el detalle de la residencia que se pasa como parametro
def detalle_residencia (request, cod):
    residencia = Residencia.objects.get(codigo = cod)
    try:
        subasta = Subasta.objects.get(codigo_residencia = cod)
    except Subasta.DoesNotExist:
        subasta = None
    finally:
        if request.method == "POST":
            monto = request.POST.get("monto")
            if monto == "":
                monto = 0
            else:
                monto = int(monto)
            if monto < subasta.monto_actual or monto < subasta.monto_inicial:
                messages.error(request, "El monto debe ser mayor al de la subasta")
            else:
                subasta.monto_actual = monto
                subasta.save()
                puja = Puja()
                puja.usuario = request.user
                from datetime import datetime
                puja.fecha_y_hora = datetime.now()
                puja.codigo_subasta = subasta
                puja.monto = monto
                puja.save()
                messages.success(request, "Puja realizada con exito")
                return redirect ("/detalle_residencia/"+ str(cod))
    pujas = list(Puja.objects.filter(codigo_subasta=subasta))
    pujas.sort(key=lambda x: x.monto, reverse=True)
    if len(pujas) > 0:
        puja_alta = pujas[0]
    else:
        puja_alta = None

    hotsales = HotSale.objects.filter(codigo_residencia=cod)

    # setear los dias alquilados para no colorearlos como disponibles en el calendario
    diasAlquilados = []
    semanasAlquiladas = Alquila.objects.filter(codigo_residencia=cod)
    for semana in semanasAlquiladas:
        elLunes = semana.fecha
        for x in range (0,7):
            dia = elLunes + timedelta(days=x)
            diasAlquilados.append(str(dia))
    primer_lunes = calcularFecha()
    semanaSubasta = Subasta.objects.filter(codigo_residencia=cod)
    for semSubasta in semanaSubasta:
        elLunes = semSubasta.semana_alquila
        for x in range (0,7):
            dia = elLunes + timedelta(days=x)
            diasAlquilados.append(str(dia))
    fecha_busqueda = primer_lunes.strftime('%Y-%m-%d')
    return (render (request, "detalle_residencia.html", {"residencia": residencia, "hotsales": hotsales, "subasta": subasta, "puja": puja_alta, "diasAlquilados": diasAlquilados, "comienzo_busqueda": fecha_busqueda}))


def administracion (request):   
    return render (request, "administracion.html")

#def listado_usuarios (request):
#    return render (request, "administracion.html")

def listado_subastas (request):
    from modelos.models import Subasta
    subastas = Subasta.objects.all()
    return render (request, "subastas.html", {"subastas": subastas})

def run_cerrar_subastas (request):
    from django.http import HttpResponseRedirect
    from django.urls import reverse
    from modelos.models import Subasta
    from application.cerrar_subasta import cerrarSubasta
    if request.method == "POST":
        codigo_subasta = request.POST.get("codigo", "")
        subasta = list(Subasta.objects.filter(codigo=codigo_subasta))
        print("cerrando subasta: ", subasta[0].codigo)
        cerrarSubasta(subasta[0])
    return HttpResponseRedirect(reverse('subastas'))

def faq_premium(request):
    try:
        subscripcion = Variables_sistema.objects.get(pk = 1)
        subscripcion = subscripcion.precio_usuario_premium
    except Variables_sistema.DoesNotExist:
        subscripcion = 0
    finally:
        return render(request, "faq_premium.html", {'subscripcion':subscripcion})