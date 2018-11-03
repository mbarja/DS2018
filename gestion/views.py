from django.shortcuts import render
import datetime
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login as dj_login
from gestion.models import TipoUsuario
from django.template.context_processors import request
from _ast import Num


def home(request):
    errors=[]
    fecha = datetime.datetime.now()
   
    if request.method == 'POST':
        
        formlogin = LoginForm(request.POST)

        if formlogin.is_valid():
            
            usuario = formlogin.cleaned_data['usuario']

            contrasenia = formlogin.cleaned_data['contrasenia']

            user = authenticate(username=usuario, password=contrasenia)
            
            if user is not None:
                
                dj_login(request, user)
                    
                base = obtenerHtmlSegunTipoUsuario(usuario)
                
                return render(request, base, {'fecha': fecha, 'usuario':usuario})
            
            else:
               
                errorlogin='El usuario o contraseña no son válidos'
                
                return render(request, 'home.html', {'fecha': fecha, 'formlogin':formlogin, 'errorlogin':errorlogin})
    else:
        formlogin = LoginForm()
        
        return render(request, 'home.html', {'fecha': fecha, 'formlogin':formlogin, 'errors':errors})
    

def obtenerHtmlSegunTipoUsuario(usuario):
    
    tipo = TipoUsuario.objects.filter(usuario=usuario).values_list('tipo',flat=True) 
    
    if tipo[0]=='D':
        return 'home_duenio.html'
    
    if tipo[0]=='T':
        return 'home_tecnico.html'
    

def registrar_tratamiento(request):
    
    errors=[]
    fecha = datetime.datetime.now()
    
    if request.user.is_authenticated:
        usuario = request.user.username
        #ELSE usuario no logueado   
       
    if request.method == 'POST':
        
        form = EquipoForm(request.POST)

        if form.is_valid():
           
            equipo = form.save(commit=False)
        
            equipo.save()
        
        else:
            
            print(form.errors)
            
            return render(request, 'alta_tratamiento.html', {'fecha': fecha, 'form':form, 'errors':errors, 'usuario':usuario})    
    
    form = EquipoForm()
    
    return render(request, 'alta_tratamiento.html', {'fecha': fecha, 'form':form, 'errors':errors, 'usuario':usuario})    

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

