from django.shortcuts import render
import datetime


# Create your views here.
def login(request):
    return render(request, 'login.html')

def home(request):
    fecha = datetime.datetime.now()
    return render(request, 'home.html', {'fecha': fecha})

def equipos(request):
    fecha = datetime.datetime.now()
    return render(request, 'equipos_general.html', {'fecha': fecha})

def home_tecnico(request):
    fecha = datetime.datetime.now()
    return render(request, 'home_tecnico.html', {'fecha': fecha})

def alquiler_equipos(request):
    fecha = datetime.datetime.now()
    return render(request, 'alquiler_equipos.html', {'fecha': fecha})

def estado_alquileres_tecnico(request):
    fecha = datetime.datetime.now()
    return render(request, 'estado_alquileres_tecnico.html', {'fecha': fecha})

def tratamientos_tecnico(request):
    fecha = datetime.datetime.now()
    return render(request, 'tratamientos_tecnico.html', {'fecha': fecha})

def equipos_tecnico(request):
    fecha = datetime.datetime.now()
    return render(request, 'equipos_tecnico.html', {'fecha': fecha})

def home_duenio(request):
    fecha = datetime.datetime.now()
    return render(request, 'home_duenio.html', {'fecha': fecha})

def equipos_duenio(request):
    fecha = datetime.datetime.now()
    return render(request, 'equipos_duenio.html', {'fecha': fecha})

def nuevo_equipo(request):
    fecha = datetime.datetime.now()
    return render(request, 'nuevo_equipo.html', {'fecha': fecha})

def tratamientos(request):
    fecha = datetime.datetime.now()
    return render(request, 'tratamientos_general.html', {'fecha': fecha})

def tratamientos_duenio(request):
    fecha = datetime.datetime.now()
    return render(request, 'tratamientos_duenio.html', {'fecha': fecha})

def calendario(request):
    fecha = datetime.datetime.now()
    return render(request, 'fechas_disponibles.html', {'fecha': fecha})

