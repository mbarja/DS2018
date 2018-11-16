from django.shortcuts import render, redirect
import datetime
from .forms import *
from gestion import *
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.models import User
from gestion.models import TipoUsuario
from django.db.models import Q
from django.template.context_processors import request
from _overlapped import NULL


def logout(request):
    dj_logout(request)
    
    fecha = datetime.datetime.now()
    formTecnico = TecnicoForm()
    formlogin = LoginForm()
        
    return render(request, 'home.html', {'fecha': fecha, 'formlogin':formlogin, 'formTecnico':formTecnico})

def home(request):
    errors=[]
    fecha = datetime.datetime.now()
   
    if request.method == 'POST':
        
        formTecnico = TecnicoForm(request.POST)

        if formTecnico.is_valid():
            
            
            usuario = formTecnico.cleaned_data['usuario']

            contrasenia = formTecnico.cleaned_data['contrasenia']

            user = authenticate(username=usuario, password=contrasenia)
            
            if user is not None:
                
                errorTecnico = 'El usuario ya existe en el sistema'
                
                return render(request, 'home.html', {'fecha': fecha, 'formTecnico':formTecnico, 'errorTecnico':errorTecnico})
            
            else:
                
                user = User.objects.create_user(username=usuario, password=contrasenia)
                
                tecnico = formTecnico.save(commit=False)
        
                formTecnico.save()
                
                dj_login(request, user)
                
                tipo = TipoUsuario(tipo='T', usuario=usuario)
                
                tipo.save()
                
                return render(request, 'home_tecnico.html', {'fecha': fecha, 'usuario':usuario})
            
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
        
        formTecnico = TecnicoForm()
        formlogin = LoginForm()
        
        return render(request, 'home.html', {'fecha': fecha, 'formlogin':formlogin, 'formTecnico':formTecnico, 'errors':errors})
    
    

def obtenerHtmlSegunTipoUsuario(usuario):
    
    tipo = TipoUsuario.objects.filter(usuario=usuario).values_list('tipo',flat=True) 
    
    if tipo[0]=='D':
        return 'home_duenio.html'
    
    if tipo[0]=='T':
        return 'home_tecnico.html'
    

def alta_equipo(request):
    
    errors=[]
    fecha = datetime.datetime.now()
    
    usuario = validarUsuarioRegistrado(request)
    
    if request.method == 'POST':
        
        form = EquipoForm(request.POST)

        if form.is_valid():
           
            equipo = form.save(commit=False)
        
            equipo.save()
            
            return render(request, 'equipo_registrado.html', {'fecha': fecha, 'usuario':usuario, 'num_serie': equipo.num_serie})
        
        else:
            
            return render(request, 'alta_equipo.html', {'fecha': fecha, 'form':form, 'errors':errors, 'usuario':usuario})    
    
    form = EquipoForm()
    
    return render(request, 'alta_equipo.html', {'fecha': fecha, 'form':form, 'errors':errors, 'usuario':usuario})    

def alta_tratamiento(request):
    
    errors=[]
    fecha = datetime.datetime.now()
    
    usuario = validarUsuarioRegistrado(request)
    
    if request.method == 'POST':
        
        form = TratamientoForm(request.POST)

        if form.is_valid():
           
            tratamiento = form.save(commit=False)
        
            tratamiento.save()
            
            return render(request, 'tratamiento_registrado.html', {'fecha': fecha, 'usuario':usuario})
        
        else:
            
            return render(request, 'alta_tratamiento.html', {'fecha': fecha, 'form':form, 'errors':errors, 'usuario':usuario})    
    
    form = TratamientoForm()
    
    return render(request, 'alta_tratamiento.html', {'fecha': fecha, 'form':form, 'errors':errors, 'usuario':usuario})    

def alta_precio_uso(request):
    errors=[]
    fecha = datetime.datetime.now()
    
    usuario = validarUsuarioRegistrado(request)
    
    if usuario==NULL:

        formlogin = LoginForm()
        
        errors.append('Debe estar logueado en el sistema para poder dar de alta un equipo')
        
        return render(request, 'home.html', {'fecha': fecha, 'formlogin':formlogin, 'errores':errors})
    
    if request.method == 'POST':
        
        form = PrecioUsoForm(request.POST)

        if form.is_valid():
           
            precioUso = form.save(commit=False)
            
            if (validarPrecioPorUso(form)):
            
                precioUso.save()
                
                return render(request, 'precio_uso_registrado.html', {'fecha': fecha, 'usuario':usuario})
            
            else:
                errors.append('Ya existe ese rango registrado para el equipo')
                return render(request, 'alta_precio_uso.html', {'fecha': fecha, 'form':form, 'errores':errors, 'usuario':usuario}) 
        
        else:
            
            return render(request, 'alta_precio_uso.html', {'fecha': fecha, 'form':form, 'errores':errors, 'usuario':usuario})    
    
    form = PrecioUsoForm()
    
    return render(request, 'alta_precio_uso.html', {'fecha': fecha, 'form':form, 'errors':errors, 'usuario':usuario})
    
def validarPrecioPorUso(form):
    
    equipo = form.cleaned_data['equipo']
    rango = form.cleaned_data['rango']
    
    precio = PrecioPorUso.objects.filter(equipo=equipo).filter(rango=rango)

    if not precio:
        return True
    
    else:
        return False
    

    
    
def alquiler_equipos(request):
    errors = []
    fecha = datetime.datetime.now()
    usuario = validarUsuarioRegistrado(request)
    
    if request.method == 'POST':
        
        form = AlquilerForm(request.POST)
        
        if form.is_valid():
            
            alquiler = validarDatosParaAlquiler(form, usuario)
            
            if not alquiler:
                errors.append('El equipo no esta disponible para las fechas elegidas')
                return render(request, 'alquiler_equipos.html', {'fecha': fecha, 'form':form, 'errores':errors, 'usuario':usuario})
                
            else:
                equipo = getattr(alquiler, 'equipo')
                desde = getattr(alquiler, 'desde')
                hasta = getattr(alquiler, 'hasta')
                return render(request, 'alquiler_reservado.html', {'fecha': fecha, 'usuario':usuario, 'equipo':equipo, 'desde': desde, 'hasta':hasta})
                
                
            
        else:
            print(form.errors)
        
    
    form = AlquilerForm()
    
    return render(request, 'alquiler_equipos.html', {'fecha': fecha, 'usuario':usuario, 'form': form})

def validarDatosParaAlquiler(form, usuario):
    
    datosEquipo = str(form.cleaned_data['equipos'])
    fechas = str(form.cleaned_data['fechas'])
    
    equipoArreglo = datosEquipo.split()
    fechasArreglo = fechas.split(' - ', 2)
    
    consultaDni = Tecnico.objects.filter(usuario=usuario).values_list('dni',flat=True)
    
    dniUsuario = consultaDni[0]
    
    equipo = equipoArreglo[0]
    format_str = '%d/%m/%Y'
    desde =  datetime.datetime.strptime(fechasArreglo[0], format_str)
    hasta = datetime.datetime.strptime(fechasArreglo[1], format_str)
    
   
    alquileres = Alquiler.objects.filter(equipo=equipo).filter(desde__range=[desde.date(), hasta.date()]).filter(hasta__range=[desde.date(), hasta.date()]).filter(~Q(estado = 'O'))
    
    if not alquileres:
        
        alquiler = registrarAlquiler(equipo, desde, hasta, dniUsuario)
        return alquiler
    else:
        return NULL

def estado_alquileres_tecnico(request):
    
    fecha = datetime.datetime.now()
    usuario = validarUsuarioRegistrado(request)
    
    consultaDni = Tecnico.objects.filter(usuario=usuario).values_list('dni',flat=True)
    
    dniUsuario = consultaDni[0]
    
    alquileres = Alquiler.objects.filter(tecnico=dniUsuario)
    
    print(alquileres)
    
    return render(request, 'estado_alquileres_tecnico.html', {'fecha': fecha, 'usuario':usuario})
   
    
def registrarAlquiler(idEquipo, desde, hasta, dniUsuario):
    
    equipo = Equipo.objects.get(num_serie=idEquipo)
    
    tecnico = Tecnico.objects.get(dni=dniUsuario)
    
    alquiler = Alquiler(tecnico=tecnico, equipo=equipo, desde=desde.date(), hasta=hasta.date(), estado='R' )
    
    alquiler.save()
    
    return alquiler


def equipos_tecnico(request):
    
    fecha = datetime.datetime.now()
    usuario = validarUsuarioRegistrado(request)
    
    equipos = Equipo.objects.all()
    
    return render(request, 'equipos_tecnico.html', {'fecha': fecha, 'usuario':usuario, 'equipos':equipos})

    
def equipos(request):
    fecha = datetime.datetime.now()
    return render(request, 'equipos_general.html', {'fecha': fecha})

def home_tecnico(request):
    fecha = datetime.datetime.now()
    usuario = validarUsuarioRegistrado(request)
    return render(request, 'home_tecnico.html', {'fecha': fecha, 'usuario':usuario})

def tratamientos_tecnico(request):
    fecha = datetime.datetime.now()
    usuario = validarUsuarioRegistrado(request)
    return render(request, 'tratamientos_tecnico.html', {'fecha': fecha, 'usuario':usuario})


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

def validarUsuarioRegistrado(request):
    
    if request.user.is_authenticated:
        
        usuario = request.user.username
        
        return usuario
    else:
        return NULL

