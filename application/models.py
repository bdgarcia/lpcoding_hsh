from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class ItemsCatalogo(models.Model):
    nombre = "nombre de residencia"
    ubicacion = "ubicacion"
    precio = "precio"
    descripcion = "descripcion"