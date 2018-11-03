from __future__ import unicode_literals
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.
UNIDADES_MEDIDA = (
        ('P', 'Pulsos'),
        ('D', 'Dias'),
    )
TIPOS_USUARIO = (
        ('C', 'Cliente'),
        ('T', 'Tecnico'),
        ('D', 'Duenio'),
    )

def no_future(value):
    today = date.today()
    if value > today:
        raise ValidationError('La fecha ingresada no puede ser a futuro')

def negativo(value):
    if value < 0:
        raise ValidationError('Este valor no puede ser negativo')
    
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
    tipo = models.CharField(max_length=1, choices=TIPOS_USUARIO)
    usuario = models.CharField(max_length=10)
    
    def __str__(self):
        return self.tipo
    
class Equipo(models.Model):
    
    num_serie = models.IntegerField(primary_key=True, unique=True, error_messages={'unique':"Ya existe un equipo con este numero de serie"})
    nombre = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    fecha_compra = models.DateField(validators=[no_future])
    precio_dia = models.IntegerField(validators=[negativo])
    periodo_mantenimiento = models.IntegerField(validators=[negativo])
    unidad_medida = models.CharField(max_length=1, choices=UNIDADES_MEDIDA)
    
    def __str__(self):
        return self.num_serie
    
    
class Tratamiento(models.Model):
    nombre = models.CharField(max_length=50)
    informacion = models.CharField(max_length=2000)
    equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    