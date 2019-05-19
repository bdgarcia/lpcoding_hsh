import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from modelos.models import Residencia
from modelos.models import Subasta
from modelos.models import Puja

from .forms import ResidenciaForm
from .forms import PujaForm

# Create your views here.
def index(request):

    residencias = Residencia.objects.filter(borrado_logico=False)

    return render(request, "index.html", {"residencias": residencias})

# Create your views here.
def test(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')

# Formulario alta residencia
def alta_residencia(request):
                                    #Agregar redireccion a pagina no disponible en caso de que
                                    #el usuario no sea admin.
    if request.method == "POST":
        form=ResidenciaForm(request.POST, request.FILES)
        if form.is_valid():
            residencia = form.save()
            residencia.save()
            return redirect("/detalle_residencia/"+ str(residencia.pk))
    else:
        form=ResidenciaForm
    return render(request,"alta_residencia.html", {'form':form})




# Formulario modificacion/baja de residencia
def mod_residencia(request, pk):
                                    #Agregar redireccion a pagina no disponible en caso de que
                                    #el usuario no sea admin.
    residencia = get_object_or_404(Residencia, pk=pk)
    if request.method == "POST" and 'btnModificar' in request.POST:
        form = ResidenciaForm(request.POST, instance=residencia) 
        if form.is_valid():
            residencia = form.save(commit=False) #por si tengo que modificar datos
            residencia.save()
            return redirect("/detalle_residencia/"+ str(residencia.pk))
    elif request.method =="POST" and "btnEliminar" in request.POST:
        form=ResidenciaForm(request.POST, instance=residencia)
        residencia=form.save(commit=False)
        residencia.borrado_logico=True
        residencia.save()
        return redirect('/')
    else:
        form = ResidenciaForm(instance=residencia)
    return render(request, 'alta_residencia.html', {'form': form})



# Muestra el detalle de la residencia que se pasa como parametro
def detalle_residencia (request, cod):
    residencia = Residencia.objects.get(codigo = cod)
    try:
        subasta = Subasta.objects.get(codigo_residencia = cod)
    except Subasta.DoesNotExist:
        subasta = None
    finally:
        if request.method == "POST":
            form = PujaForm(request.POST)
            puja = form.save(commit=False)
            subasta.monto_actual = puja.monto
            puja.save()
            subasta.save()
            return redirect ("/detalle_residencia/"+ str(cod))
        else:
            form = PujaForm(request.POST)
    return (render (request, "detalle_residencia.html", {"residencia": residencia, "subasta": subasta, "form": form}))

# Redirecciona a la pagina de inicio si no se le pasan parametros a detalle_residencia
def detalle_residencia_solo (request):
    return redirect("index")




def administracion (request):   
    return render (request, "administracion.html")

def listado_usuarios (request):
    return render (request, "administracion.html")

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
