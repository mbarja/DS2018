from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Tecnico(models.Model):
    dni = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.IntegerField()
    mail = models.CharField(max_length=50)
    usuario = models.CharField(max_length=10)
    contrasenia = models.CharField(max_length=30)
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.IntegerField()
    mail = models.CharField(max_length=50)
    usuario = models.CharField(max_length=10)
    contrasenia = models.CharField(max_length=30)

class TipoUsuario(models.Model):
    TIPOS_USUARIO = (
        ('C', 'Cliente'),
        ('T', 'Tecnico'),
        ('D', 'Duenio'),
    )
    tipo = models.CharField(max_length=1, choices=TIPOS_USUARIO)
    usuario = models.CharField(max_length=10)
    
    def __str__(self):
        return self.tipo
    