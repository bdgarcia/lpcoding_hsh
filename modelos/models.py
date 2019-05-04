from django.db import models

# Create your models here.

class Residencia (models.Model):
    codigo = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length =50)
    ubicacion = models.CharField(max_length = 100)
    descripcion = models.TextField()
    precio = models.FloatField()
    monto_minimo_subasta = models.FloatField()
    foto = models.FileField(default=None, blank=True, null=True) 
    borrado_logico = models.BooleanField(default=False)

    def content_file_name(instance, filename):
        import os
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (instance.codigo, ext)
        return os.path.join('uploads', filename)

class Usuario (models.Model):
    nombre = models.CharField(max_length = 30)
    apellido = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 100)
    fecha_nacimiento = models.DateField()
    contraseña = models.CharField(max_length = 30)
    tarjeta_credito = models.CharField(max_length = 30)
    #membresia
    creditos = models.IntegerField()

class Subasta (models.Model):
    codigo_residencia = models.ForeignKey("Residencia", on_delete=models.CASCADE)
    monto_actual = models.FloatField()
    monto_inicial = models.FloatField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    codigo = models.AutoField(primary_key = True)

class Puja (models.Model):
    email = models.EmailField(max_length = 100)
    monto = models.FloatField()
    fecha_y_hora = models.DateTimeField()
    codigo_subasta = models.ForeignKey("Subasta", on_delete = models.CASCADE)

class Alquila (models.Model):
    email_usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    codigo_residencia = models.ForeignKey("Residencia", on_delete= models.CASCADE)
    fecha = models.DateField()
    precio = models.FloatField()
    #modo ----> depende de la membresia del usuario