from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

# Create your models here.

def get_file_path(instance, filename):
    """Cambia el nombre del archivo a el nombre y la ubicacion"""
    ext = filename.split('.')[-1]
    filename = "%s-%s.%s" % (instance.nombre, instance.ubicacion, ext)
    return os.path.join(filename)

class Residencia (models.Model):
    codigo = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length =50)
    ubicacion = models.CharField(max_length = 100, unique=True)
    descripcion = models.TextField()
    precio = models.FloatField()
    monto_minimo_subasta = models.FloatField()
    foto = models.FileField(upload_to=get_file_path,default=None, blank=True, null=True) 
    borrado_logico = models.BooleanField(default=False)

class Usuario (AbstractUser):
    nombre = models.CharField(max_length = 30)
    apellido = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 100, unique= True)
    fecha_nacimiento = models.DateField()
    #
    # https://github.com/dldevinc/django-credit-cards
    numero_tarjeta = CardNumberField(_("Card number"))
    vencimiento_tarjeta = CardExpiryField(_('expiration date'))
    codigo_tarjeta = SecurityCodeField(_('security code'))
    #
    creditos = models.IntegerField(default=2)
    type = models.CharField(max_length = 30)
    REQUIRED_FIELDS = ['fecha_nacimiento', 'email', 'creditos']

class Subasta (models.Model):
    codigo_residencia = models.ForeignKey("Residencia", on_delete=models.CASCADE)
    monto_actual = models.FloatField(default=0.0)
    monto_inicial = models.FloatField(default=0.0)
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

class Variables_sistema (models.Model):
    precio_usuario_comun = models.FloatField(default=0.0)
    precio_usuario_premium = models.FloatField(default=0.0)