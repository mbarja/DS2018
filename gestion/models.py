from __future__ import unicode_literals
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.
UNIDADES_MEDIDA = (
        ('P', 'Pulsos'),
        ('D', 'Dias'),
    )

ESTADOS = (
        ('R', 'Reservado'),
        ('C', 'Confirmado'),
        ('S', 'Esperando Confirmacion'),
        ('E', 'En curso'),
        ('O', 'Cancelado'),
        ('F', 'Finalizado'),
        ('P', 'Pagado'),
    )
TIPOS_USUARIO = (
        ('C', 'Cliente'),
        ('T', 'Tecnico'),
        ('D', 'Duenio'),
    )
MARCAS_EQUIPOS = (
        ('C', 'Candela'),
        ('V', 'Venus Legacy'),
    )

def no_future(value):
    today = date.today()
    if value > today:
        raise ValidationError('La fecha ingresada no puede ser a futuro')
    
def no_past(value):
    today = date.today()
    if value < today:
        raise ValidationError('La fecha ingresada no puede ser pasado')

def negativo(value):
    if value < 0:
        raise ValidationError('Este valor no puede ser negativo')
    
class Tecnico(models.Model):
    dni = models.IntegerField(primary_key=True, unique=True, error_messages={'unique':"Ya existe un usuario con este DNI"})
    nombre = models.CharField(max_length=70)
    direccion = models.CharField(max_length=50)
    telefono = models.BigIntegerField()
    mail = models.CharField(max_length=50)
    usuario = models.CharField(max_length=10,  unique=True, error_messages={'unique':"Ya existe un tecnico con ese usuario"})
    contrasenia = models.CharField(max_length=30)
    
    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.BigIntegerField()
    mail = models.CharField(max_length=50)
    usuario = models.CharField(max_length=10)
    contrasenia = models.CharField(max_length=30)
    
    def __str__(self):
        return '%s %s' % (self.nombre, self.telefono)
    
class Equipo(models.Model):
    
    num_serie = models.IntegerField(primary_key=True, unique=True, error_messages={'unique':"Ya existe un equipo con este numero de serie"})
    nombre = models.CharField(max_length=50)
    marca = models.CharField(max_length=1, choices=MARCAS_EQUIPOS)
    fecha_compra = models.DateField(validators=[no_future])
    precio_dia = models.IntegerField(validators=[negativo])
    periodo_mantenimiento = models.IntegerField(validators=[negativo])
    unidad_medida = models.CharField(max_length=1, choices=UNIDADES_MEDIDA)
    
    def __str__(self):
        return '%s %s' % (self.num_serie, self.nombre)
    
    
class Tratamiento(models.Model):
    nombre = models.CharField(max_length=50, unique=True, error_messages={'unique':"Ya existe un tratamiento con este nombre"})
    informacion = models.CharField(max_length=2000)

    def __str__(self):
        return self.nombre

class PrecioPorUso(models.Model):
    equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE)
    precio = models.FloatField(validators=[negativo])
    rango = models.BigIntegerField(validators=[negativo])
    
class EquipoTratamiento(models.Model):
    equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE)
    tratamiento = models.ForeignKey('Tratamiento', on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s %s' % (self.equipo, self.tratamiento)
    
class Alquiler(models.Model):
    tecnico = models.ForeignKey('tecnico', null=True, blank=True,on_delete=models.CASCADE)
    equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE)
    desde = models.DateField(validators=[no_past])
    hasta = models.DateField(validators=[no_past])
    estado = models.CharField(max_length=1, choices=ESTADOS)
    estado_inicial = models.BigIntegerField(null=True, blank=True,validators=[negativo])
    estado_final = models.BigIntegerField(null=True, blank=True, validators=[negativo])
    precio = models.FloatField(validators=[negativo])
    precio_exceso = models.FloatField(validators=[negativo], null=True, blank=True)
    pagado = models.FloatField(validators=[negativo], null=True, blank=True)
    
    def __str__(self):
        return '%s %s' % (self.equipo, self.estado)

class Mantenimiento(models.Model):
    equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE)
    fecha = models.DateField(validators=[no_future])
    descripcion = models.CharField(max_length=2000)
    
    def __str__(self):
        return '%s %s' % (self.equipo, self.fecha)
    
class Turno(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    tratamiento = models.ForeignKey('tratamiento', on_delete=models.CASCADE)
    fecha = models.DateField(validators=[no_past])
    
    def __str__(self):
        return '%s %s' % (self.cliente, self.tratamiento)
    

    
    
    