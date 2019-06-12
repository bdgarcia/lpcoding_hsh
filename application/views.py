import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from modelos.models import Residencia
from modelos.models import Subasta
from modelos.models import Puja
from modelos.models import Usuario
from modelos.models import Alquila
from django.contrib.auth import login
from creditcards import types

from .forms import ResidenciaForm, UsuarioForm
from datetime import date, timedelta, datetime
# Create your views here.

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 6
    return d + timedelta(days_ahead)

def allmondays(fecha, hasta):
   d = datetime.strptime(fecha, '%Y-%m-%d')
   d = next_weekday(d, 1)
   end =  datetime.strptime(hasta, '%Y-%m-%d')
   aux = []
   while d <= end:
       aux.append(d.date())
       d = d + timedelta(days = 7)
   return aux


def index(request):
    residencias = Residencia.objects.filter(borrado_logico=False)
    subastas = Subasta.objects.all()
    if request.method == 'GET': # If the form is submitted
        if request.GET.get('parametro'):
            criteria = request.GET.get('criteria')
            parametro = request.GET.get('parametro')
            if criteria == "nombre":
                residencias = residencias.filter(nombre=parametro)
            if criteria == "ubicacion":
                residencias = residencias.filter(ubicacion=parametro)

        if request.GET.get('enSubasta'):
            codigos_subasta = []
            for subasta in subastas:
                codigos_subasta.append(subasta.codigo_residencia.codigo)
            residencias = residencias.filter(codigo__in=codigos_subasta)

        if request.GET.get('fecha') or request.GET.get('hasta'):
            fecha_desde = date.today()
            fecha_hasta = date.today() + timedelta(days=60)

            if request.GET.get('fecha'):
                fecha_desde = request.GET.get('fecha')

            if request.GET.get('hasta'):
                fecha_hasta = request.GET.get('hasta')

            todosLosLunes = allmondays(fecha_desde, fecha_hasta)
            resultado = []
            for residencia in residencias:
                for unLunes in todosLosLunes:
                    alquileres = Alquila.objects.filter(codigo_residencia=residencia)
                    isRented = alquileres.filter(fecha=unLunes)
                    if (not isRented.exists()):
                        if residencia not in resultado:
                            resultado.append(residencia)
            residencias = resultado

    return render(request, "index.html", {"residencias": residencias, "subastas": subastas})

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
        if request.method=="POST":
            form=UsuarioForm(request.POST, request.FILES)
            if form.is_valid():
                usuario=form.save(commit=False)
                #Para alta de admins: if usuario.type != admin:
                usuario.type="comun"
                usuario.set_password(usuario.password)
                usuario.save()
                if not request.user.is_authenticated:
                    login(request, usuario)
                messages.success(request, 'El usuario fue creado correctamente')
                return redirect("/usuario/"+str(usuario.pk))
        else:
                form=UsuarioForm
        return (render(request, "alta_usuario.html", {"form":form}))




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
    return (render(request, "detalle_usuario.html", {"usuario": usuario, "alquileres": alquileres, "marca": marca_tarjeta, "vencimiento_creditos":aux}))



# Muestra el listado de usuarios, permitiendo ordenar por el criterio deseado
def listado_usuarios(request):
    if (request.user.is_authenticated and request.user.type == "admin"):
        users = Usuario.objects.all()
        return (render (request, "listado_usuarios.html" , {"users": users}))
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

    # setear los dias alquilados para no colorearlos como disponibles en el calendario
    diasAlquilados = []
    semanasAlquiladas = Alquila.objects.filter(codigo_residencia=cod)
    for semana in semanasAlquiladas:
        elLunes = semana.fecha
        for x in range (0,7):
            dia = elLunes + timedelta(days=x)
            diasAlquilados.append(str(dia))

    return (render (request, "detalle_residencia.html", {"residencia": residencia, "subasta": subasta, "puja": puja_alta, "diasAlquilados": diasAlquilados}))


# Redirecciona a la pagina de inicio si no se le pasan parametros a detalle_residencia
def detalle_residencia_solo (request):
    return redirect("index")

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
