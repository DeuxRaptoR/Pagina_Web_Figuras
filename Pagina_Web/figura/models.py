from django.db import models


class Usuario(models.Model):
    nombre_usuario = models.TextField(max_length=30)
    contraseña_usuario = models.TextField(max_length=30)

    
class Figura(models.Model):
    nombre_figura = models.TextField(max_length=200)
    personaje = models.TextField(max_length=40)
    imagen = models.ImageField(upload_to="imagenes/", null=True, blank=True )
    fabricante = models.TextField (max_length=60)
    precio = models.IntegerField (null=False)
    tamaño = models.IntegerField (null=False)
    material = models.TextField (max_length=30)
    accesorios = models.TextField (max_length=600)
    categoria = models.TextField (max_length=50)



# Create your models here.
