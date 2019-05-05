import requests
from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from modelos.models import Residencia


# Create your views here.
def index(request):

    residencias = Residencia.objects.all()

    return render(request, "index.html", {"residencias": residencias})

# Create your views here.
def test(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
