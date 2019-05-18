from django.contrib.auth.models import AbstractUser
from django.db import models
import os

# Create your models here.

def get_file_path(instance, filename):
    """Cambia el nombre del archivo a el nombre y la ubicacion"""
    ext = filename.split('.')[-1]
    filename = "%s-%s.%s" % (instance.nombre, instance.ubicacion, ext)
    return os.path.join(filename)

class Residencia (models.Model):
    codigo = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length =50)
    ubicacion = models.CharField(max_length = 100, unique = True)
    descripcion = models.TextField()
    precio = models.FloatField()
    monto_minimo_subasta = models.FloatField()
    foto = models.FileField(upload_to=get_file_path,default=None, blank=True, null=True) 
    borrado_logico = models.BooleanField(default=False)

class Usuario (AbstractUser):
    nombre = models.CharField(max_length = 30)
    apellido = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 100)
    fecha_nacimiento = models.DateField()
    tarjeta_credito = models.CharField(max_length = 30)
    #membresia
    creditos = models.IntegerField()
    type = models.CharField(max_length = 30)
    REQUIRED_FIELDS = ['fecha_nacimiento', 'email', 'creditos']

class Subasta (models.Model):
    codigo_residencia = models.ForeignKey("Residencia", on_delete=models.CASCADE)
    monto_actual = models.FloatField()
    monto_inicial = models.FloatField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    semana_alquila = models.DateField()
    codigo = models.AutoField(primary_key = True)

class Puja (models.Model):
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    monto = models.FloatField()
    fecha_y_hora = models.DateTimeField()
    codigo_subasta = models.ForeignKey("Subasta", on_delete = models.CASCADE)

class Alquila (models.Model):
    email_usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    codigo_residencia = models.ForeignKey("Residencia", on_delete= models.CASCADE)
    fecha = models.DateField()
    precio = models.FloatField()
    #modo ----> depende de la membresia del usuario