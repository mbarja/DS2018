from django.shortcuts import render, redirect
import datetime
from .forms import *
from gestion import *
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.template.context_processors import request
from _overlapped import NULL
from django.shortcuts import get_object_or_404, redirect, render, reverse
from http.cookiejar import request_path
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail

def not_in_tecnicos_group(user):
    if user:
        return user.groups.filter(name='tecnicos').count() != 0
    return False

def not_in_clientes_group(user):
    if user:
        return user.groups.filter(name='clientes').count() != 0
    return False

def logout_view(request, next_page):
    logout(request)
    return redirect(next_page, request.path)


def home(request):
    errors=[]
    fecha = datetime.datetime.now()
   
    if request.method == 'POST':
        
        formTecnico = TecnicoForm(request.POST)
        

        if formTecnico.is_valid():
            
            usuario = formTecnico.cleaned_data['usuario']

            contrasenia = formTecnico.cleaned_data['contrasenia']

            user = User.objects.filter(username=usuario)
            
            if not user:
                
                user = User.objects.create_user(username=usuario, password=contrasenia)
                
                tecnico = formTecnico.save(commit=False)
        
                formTecnico.save()
                
                grupoTecnico = Group.objects.get(name='tecnicos') 
                grupoTecnico.user_set.add(user)
                
                dj_login(request, user)
                
                
                return render(request, 'home_tecnico.html', {'fecha': fecha, 'usuario':usuario})
                
            
            else:
                
                errors.append('El usuario ya existe en el sistema')
                
                return render(request, 'home.html', {'fecha': fecha, 'formTecnico':formTecnico, 'errores':errors})
                
        else:
            
            formCliente = ClienteForm(request.POST)
            
            if formCliente.is_valid():
                
                usuario = formCliente.cleaned_data['usuario']
    
                contrasenia = formCliente.cleaned_data['contrasenia']
    
                user = User.objects.filter(username=usuario)
                
                if not user:
                    
                    user = User.objects.create_user(username=usuario, password=contrasenia)
                    
                    Cliente = formCliente.save(commit=False)
            
                    formCliente.save()
                    
                    grupoCliente = Group.objects.get(name='clientes') 
                    grupoCliente.user_set.add(user)
                    
                    dj_login(request, user)
                    
                    return render(request, 'home_cliente.html', {'fecha': fecha, 'usuario':usuario})
                
                else:
                    
                    errors.append('El usuario ya existe en el sistema')
                    
                    return render(request, 'home.html', {'fecha': fecha, 'formCliente':formCliente, 'errores':errors})
                    
        
            else:
                
                formlogin = LoginForm(request.POST)
                
                if formlogin.is_valid():
            
                    usuario = formlogin.cleaned_data['user']
        
                    contrasenia = formlogin.cleaned_data['pswd']
        
                    user = authenticate(username=usuario, password=contrasenia)
                    
                    if user is not None:
                        
                        dj_login(request, user)
                            
                        base = obtenerHtmlSegunTipoUsuario(user)
                        
                        return render(request, base, {'fecha': fecha, 'usuario':usuario})
                    
                    else:
                       
                        errors.append('El usuario o contraseña no son válidos')
                        
                        return render(request, 'home.html', {'fecha': fecha, 'formlogin':formlogin, 'errores':errors})
    else:
        
        formTecnico = TecnicoForm()
        formlogin = LoginForm()
        formCliente = ClienteForm()
        
        return render(request, 'home.html', {'fecha': fecha, 'formlogin':formlogin, 'formTecnico':formTecnico, 'formCliente':formCliente, 'errors':errors})
        

def obtenerHtmlSegunTipoUsuario(user):
    
    if user:
        if user.groups.filter(name='tecnicos').count() != 0:
            return 'home_tecnico.html'
        elif user.groups.filter(name='clientes').count() != 0:
            return 'home_cliente.html'
        else:
            return 'home_duenio.html'
    return False   

@login_required 
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def alta_equipo(request):
    
    errors=[]
    fecha = datetime.datetime.now()
    
    usuario = request.user.username
    
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

@login_required 
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def alta_tratamiento(request):
    
    errors=[]
    fecha = datetime.datetime.now()
    
    usuario = request.user.username
    
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

@login_required 
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def alta_precio_uso(request):
    errors=[]
    fecha = datetime.datetime.now()
    
    usuario = request.user.username
    
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

@login_required 
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')    
def registrar_mantenimiento(request):
    errors=[]
    fecha = datetime.datetime.now()
    
    usuario = request.user.username
    
    if request.method == 'POST':
        
        form = MantenimientoForm(request.POST)

        if form.is_valid():
           
            mantenimiento = form.save(commit=False)
            
            if (validarMantenimiento(form)):
            
                mantenimiento.save()
                
                return render(request, 'mantenimiento_registrado.html', {'fecha': fecha, 'usuario':usuario})
            
            else:
                errors.append('Ya existe un mantenimiento registrado para el equipo en esa fecha')
                return render(request, 'registrar_mantenimiento.html', {'fecha': fecha, 'form':form, 'errores':errors, 'usuario':usuario}) 
        
        else:
            
            return render(request, 'registrar_mantenimiento.html', {'fecha': fecha, 'form':form, 'errores':errors, 'usuario':usuario})    
    
    form = MantenimientoForm()
    
    return render(request, 'registrar_mantenimiento.html', {'fecha': fecha, 'form':form, 'errors':errors, 'usuario':usuario})

def validarMantenimiento(form):
    equipo = form.cleaned_data['equipo']
    fecha = form.cleaned_data['fecha']
    
    mantenimiento = Mantenimiento.objects.filter(equipo=equipo).filter(fecha=fecha)

    if not mantenimiento:
        return True
    
    else:
        return False
    
@login_required 
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')    
def alta_equipo_tratamiento(request):
    errors=[]
    fecha = datetime.datetime.now()
    
    usuario = request.user.username
    
    if request.method == 'POST':
        
        form = EquipoTratamientoForm(request.POST)

        if form.is_valid():
           
            equipoTratamiento = form.save(commit=False)
            
            if (validarEquipoTratamiento(form)):
            
                equipoTratamiento.save()
                
                return render(request, 'equipo_tratamiento_registrado.html', {'fecha': fecha, 'usuario':usuario})
            
            else:
                errors.append('Ya existe ese tratamiento asociado al equipo')
                return render(request, 'alta_equipo_tratamiento.html', {'fecha': fecha, 'form':form, 'errores':errors, 'usuario':usuario}) 
        
        else:
            
            return render(request, 'alta_equipo_tratamiento.html', {'fecha': fecha, 'form':form, 'errores':errors, 'usuario':usuario})    
    
    form = EquipoTratamientoForm()
    
    return render(request, 'alta_equipo_tratamiento.html', {'fecha': fecha, 'form':form, 'errors':errors, 'usuario':usuario})
       
def validarEquipoTratamiento(form):
    
    equipo = form.cleaned_data['equipo']
    tratamiento = form.cleaned_data['tratamiento']
    
    relacion = EquipoTratamiento.objects.filter(equipo=equipo).filter(tratamiento=tratamiento)

    if not relacion:
        return True
    
    else:
        return False

@login_required 
@user_passes_test(not_in_tecnicos_group, login_url='/home/')    
def alquiler_equipos(request):
    errors = []
    fecha = datetime.datetime.now()
    usuario = request.user.username
    
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

@login_required 
@user_passes_test(not_in_tecnicos_group, login_url='/home/') 
def editar_datos_tecnico(request):
    fecha = datetime.datetime.now()
    usuario = request.user.username
    
    if request.method == 'POST':
        
        dniTecnico = request.POST['id_tecnico']
        
        form = TecnicoModificarForm(data=request.POST)
    
        if form.is_valid():
            
            instance = form.save(commit=False)
            
            instance.dni = dniTecnico
            
            instance.usuario = usuario
            
            contrasenia = form.cleaned_data['contrasenia']
            
            user = request.user
            
            user.set_password(contrasenia)
            
            user.save()
            
            update_session_auth_hash(request, user)
            
            instance.save()
            
            return render(request, 'datos_editados_tecnico.html', {'fecha': fecha, 'usuario':usuario})
    
        else:
            
            return render(request, 'editar_datos_tecnico.html', {'fecha':fecha, 'usuario':usuario, 'form':form})
        
    
    tecnico = Tecnico.objects.get(usuario=usuario)
    
    form = TecnicoModificarForm(instance=tecnico)

    
    return render(request, 'editar_datos_tecnico.html', {'fecha':fecha, 'dni':tecnico.dni, 'usuario': usuario, 'form':form})
    
@login_required 
@user_passes_test(not_in_tecnicos_group, login_url='/home/')
def estado_alquileres_tecnico(request):
    
    fecha = datetime.datetime.now()
    usuario = request.user.username
    
    if 'id_alquiler' in request.GET:
        id_alquiler = request.GET['id_alquiler']
        
        alquiler = Alquiler.objects.get(id=id_alquiler)
        
        alquiler.id = id_alquiler
        
        if 'confirmar' in request.GET:
            alquiler.estado = 'C'
        
        if 'cancelar' in request.GET:
            alquiler.estado = 'O'
        
        alquiler.save()
            
    
    consultaDni = Tecnico.objects.filter(usuario=usuario).values_list('dni',flat=True)
    
    dniUsuario = consultaDni[0]
    
    alquileres = Alquiler.objects.filter(tecnico=dniUsuario).order_by('-id')
    
    precios = calcularPreciosAlquileres(alquileres)
    
    excesos = obtenerExcesosPorUso()
    
    return render(request, 'estado_alquileres_tecnico.html', {'fecha': fecha, 'usuario':usuario, 'alquileres':alquileres, 'precios':precios, 'excesos': excesos})

def calcularPreciosAlquileres(alquileres):
    precios = []
    
    for alquiler in alquileres:
        
        equipo = getattr(alquiler, 'equipo')
        precio = getattr(equipo, 'precio_dia')
        desde = getattr(alquiler, 'desde')
        hasta = getattr(alquiler, 'hasta')
        
        cantidad_dias = (hasta - desde).days

        precio = {'alquiler':alquiler, 'precio':(cantidad_dias*precio)}
        precios.append(precio)
        
    return precios
           
def registrarAlquiler(idEquipo, desde, hasta, dniUsuario):
    
    equipo = Equipo.objects.get(num_serie=idEquipo)
    
    tecnico = Tecnico.objects.get(dni=dniUsuario)
    
    alquiler = Alquiler(tecnico=tecnico, equipo=equipo, desde=desde.date(), hasta=hasta.date(), estado='R' )
    
    alquiler.save()
    
    return alquiler

@login_required 
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def reservas(request):
    errors = []
    fecha = datetime.datetime.now()
    usuario = request.user.username
    
    if 'id_alquiler' in request.GET:
        
        id_alquiler = request.GET['id_alquiler']
        
        alquiler = Alquiler.objects.get(id=id_alquiler)
        
        alquiler.id = id_alquiler
        
        if 'iniciar' in request.GET:
            #no pueden estar mas de un equipo en curso al mismo tiempo
            chequearAlquiler =  Alquiler.objects.filter(equipo=alquiler.equipo).filter(estado='E').filter(~Q(id = alquiler.id))
            
            if not chequearAlquiler:
                alquiler.estado = 'E'
                alquiler.estado_inicial = obtenerEstadoInicial(alquiler.equipo)
            else: 
                errors.append('Ya hay alquiler en curso para el equipo '+str(alquiler.equipo))
        
        if 'finalizar' in request.GET:
            estadoFinal = request.GET['estado_final_valor']
            if estadoFinal:
                alquiler.estado_final = estadoFinal
                alquiler.estado = 'F'
            else:
                nombreEquipo = alquiler.equipo

                errors.append('Debe ingresar un estado final para poder finalizar el alquiler del equipo '+str(nombreEquipo))
                
        if 'solicitar' in request.GET:
            
            tecnico = Tecnico.objects.get(nombre=alquiler.tecnico)
            
            enviarMail(alquiler,tecnico)
            
            alquiler.estado = 'S'
            
        alquiler.save()
    
    cancelarReservasVencidas()
    reservas = Alquiler.objects.all().order_by('-id')
    excesos = obtenerExcesosPorUso()
    return render(request, 'reservas.html', {'fecha': fecha, 'usuario':usuario, 'reservas':reservas, 'excesos':excesos, 'errores':errors})

def cancelarReservasVencidas():
    
    reservas = Alquiler.objects.filter(Q(estado='S') | Q(estado='R'))
    
    for reserva in reservas:
        
        if reserva.desde <= date.today():
                reserva.estado='O'
                reserva.save()
            

def enviarMail(alquiler,tecnico):
    
    mensaje = 'Se solicita confirmar el alquiler del equipo '+str(alquiler.equipo)+'. Para las fechas '+ str(alquiler.desde)+' - '+str(alquiler.hasta)+'. Recuerde que las reservas se deben CONFIRMAR hasta un dia antes de la fecha de inicio.'
    send_mail(
    'Confirmacion de alquiler',
    mensaje,
    'beauty.rent.info@gmail.com',
    [str(tecnico.mail)],
    fail_silently=False,
)
    
def obtenerExcesosPorUso():
    
    excesos = []
    
    alquileres = Alquiler.objects.filter(estado='F')
    
    for alquiler in alquileres:
        
        pulsosUtilizados = (alquiler.estado_final - alquiler.estado_inicial)
        
       
        preciosPorUso = PrecioPorUso.objects.filter(equipo = alquiler.equipo).order_by('rango')
        
        precioPorExceso = 0
        rango=0
        
        for precio in preciosPorUso:
            
            if pulsosUtilizados > precio.rango:
                
                precioPorExceso = precio.precio
                rango = precio.rango
        
        
        pulsosDeMas = pulsosUtilizados - rango
        
        if rango != 0:
            
           excesos.append({'alquiler':alquiler, 'precio':(pulsosDeMas*precioPorExceso)})     
               
        
    return excesos

def obtenerEstadoInicial(equipo):
    
    if equipo.marca == 'V':
        return '0'
    else:
    
        alquiler = Alquiler.objects.filter(equipo=equipo).filter(estado='F').order_by('-hasta')[:1]
        
        if not alquiler:
            return '0'
        else:
            for a in alquiler:
                return getattr(a, 'estado_final')

@login_required 
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def equipos_duenio(request):
    fecha = datetime.datetime.now()
    usuario = request.user.username
    
    if request.method == 'GET':
        if 'id_equipo' in request.GET:
            
            num_serie = request.GET['id_equipo']
            
            if 'editar' in request.GET:
                
                equipo = Equipo.objects.get(num_serie=num_serie)
                
                form = EquipoModificarForm(instance=equipo)
                
                return render(request, 'equipo_modificar.html', {'fecha':fecha, 'usuario':usuario, 'form':form, 'num_serie': num_serie})
            
            
        
    if request.method == 'POST':
        
        num_serie = request.POST['num_serie2']
        
        form = EquipoModificarForm(data=request.POST)
    
        if form.is_valid():
            
            instance = form.save(commit=False)
            
            instance.num_serie = num_serie
            
            instance.save()
            
            return render(request, 'equipo_modificado.html', {'fecha': fecha, 'usuario':usuario})
    
        else:
            
            return render(request, 'equipo_modificar.html', {'fecha':fecha, 'usuario':usuario, 'form':form})
        
    
    equipos = Equipo.objects.all()
    
    estados = obtenerEstadosEquipos(equipos)
    
    pulsos = obtenerPulsosParaMantenimiento(equipos)
    
    return render(request, 'equipos_duenio.html', {'fecha': fecha, 'usuario':usuario, 'equipos':equipos, 'estados':estados, 'pulsos': pulsos})

@login_required 
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def editarPreciosPorUso(request):
    fecha = datetime.datetime.now()
    usuario = request.user.username
    
    mensaje = ""
    
    equipos = Equipo.objects.all()
    
    if request.method == 'GET':
        
        if 'equipo' in request.GET:
            
            num_serie = request.GET['equipo']
            
            if 'buscar' in request.GET:
                
                equipoSeleccionado = Equipo.objects.get(num_serie=num_serie)
                
                preciosPorUso = PrecioPorUso.objects.filter(equipo=num_serie)
                
                return render(request, 'editar_precio_uso.html', {'fecha': fecha, 'usuario':usuario, 'equipoSeleccionado':equipoSeleccionado, 'precios':preciosPorUso, 'num_serie':num_serie})
                
        if 'filtrarPrecio' in request.GET:
                
            idPrecio = request.GET['precio']
            rango = request.GET['rango']
            precio = request.GET['nuevoPrecio']
            
            num_serie = request.GET['num_serie']
            
            precioSeleccionado = PrecioPorUso.objects.get(id=idPrecio)
            precioSeleccionado.rango=rango
            precioSeleccionado.precio=precio
            precioSeleccionado.save()
            
            equipoSeleccionado = Equipo.objects.get(num_serie=num_serie)
            
            mensaje = 'Se modifico exitosamente el valor del rango: '+rango+ '- Precio:$ '+precio+ '. Del equipo '+ str(getattr(equipoSeleccionado, 'num_serie'))
            

    return render(request, 'editar_precio_uso.html', {'fecha': fecha, 'usuario':usuario, 'equipos':equipos, 'mensaje':mensaje})

@login_required 
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def obtenerEstadosEquipos(equipos):   
    hoy = datetime.datetime.now()
    estados=[]
    
    for equipo in equipos:
        
        alquileres = Alquiler.objects.filter(equipo=equipo).filter(desde__lte= hoy).filter(hasta__gte= hoy).filter(~Q(estado = 'O')).filter(~Q(estado = 'F'))
        
        if not alquileres:
            estado= {'equipo':equipo, 'estado':'Libre'}
            estados.append(estado)
        
        else:
            for alquiler in alquileres:
                
                estadoAlquiler = getattr(alquiler, 'estado')
                if estadoAlquiler=='R':
                    estadoAlquiler = 'Reservado'
                if estadoAlquiler=='C':
                    estadoAlquiler = 'Confirmado'
                if estadoAlquiler=='E':
                    estadoAlquiler = 'En Curso'
                
                estado = {'equipo':equipo, 'estado':estadoAlquiler}
                estados.append(estado)
            
    return estados  

def obtenerPulsosParaMantenimiento(equipos):
    mantenimientos = []
    pulsosUsados=0
    
    for equipo in equipos:
        
        equipoMantenimiento = (getattr(equipo, 'periodo_mantenimiento'))
        
        alquileres = Alquiler.objects.filter(equipo=equipo).filter(Q(estado='F') | Q(estado='E')).order_by('-hasta')[:1]
        
        if not alquileres:
            pulsosusados = 0 
        
        else:
            for alquiler in alquileres:
                if getattr(alquiler, 'estado')=='F':
                    pulsosUsados = getattr(alquiler, 'estado_final')
                    
                else:
                    pulsosUsados = getattr(alquiler, 'estado_inicial')
                    
        #cuando haya mantenimientos sumarle esa cantidad (equipoMantenimiento * cantidad de mantenimientos Realizados)
        
        mantenimientos.append({'equipo':equipo, 'pulsos':(equipoMantenimiento-pulsosUsados)})
        
    return mantenimientos

@login_required 
@user_passes_test(not_in_tecnicos_group, login_url='/home/')
def equipos_tecnico(request):
    
    fecha = datetime.datetime.now()
    usuario = request.user.username
    
    equipos = Equipo.objects.all()
    
    recargos = PrecioPorUso.objects.all()

    return render(request, 'equipos_tecnico.html', {'fecha': fecha, 'usuario':usuario, 'equipos':equipos, 'recargos':recargos})

@login_required 
@user_passes_test(not_in_tecnicos_group, login_url='/home/')    
def tratamientos_tecnico(request):
    fecha = datetime.datetime.now()
    usuario = request.user.username
    
    equipos = EquipoTratamiento.objects.all()
    tratamientos = Tratamiento.objects.all()
    
    return render(request, 'tratamientos_tecnico.html', {'fecha': fecha, 'tratamientos': tratamientos, 'equipos':equipos, 'usuario':usuario})
@login_required 
@user_passes_test(not_in_clientes_group, login_url='/home/')
def tratamientos_cliente(request):
    fecha = datetime.datetime.now()
    usuario = request.user.username
    
    tratamientos = Tratamiento.objects.all()
    
    
    return render(request, 'tratamientos_cliente.html', {'fecha': fecha, 'tratamientos': tratamientos, 'usuario':usuario})

@login_required 
@user_passes_test(not_in_clientes_group, login_url='/home/')
def reservar_turno(request):
    errors = []
    fecha = datetime.datetime.now()
    usuario = request.user.username
    
    if request.method == 'POST':
        
        form = TurnoForm(request.POST)
        
        if form.is_valid():
            
            turno = validarDatosParaTurno(form, usuario)
            
            if not turno:
                
                errors.append('Ya ha reservado un turno para ese tratamiento y esa fecha')
                
                return render(request, 'reservar_turno.html', {'fecha': fecha, 'form':form, 'errores':errors, 'usuario':usuario})
                
            else:
                tratamiento = getattr(turno, 'tratamiento')
                fechaTratamiento = getattr(turno, 'fecha')
                return render(request, 'turno_registrado.html', {'fecha': fecha, 'usuario':usuario, 'tratamiento':tratamiento,'fechaTratamiento':fechaTratamiento})
            
        else:
            print(form.errors)
        
    
    form = TurnoForm()
    
    return render(request, 'reservar_turno.html', {'fecha': fecha, 'tratamientos': tratamientos, 'usuario':usuario, 'form': form})

def validarDatosParaTurno(form, usuario):
    
    nombreTratamiento = form.cleaned_data['tratamiento']
    datosfecha = form.cleaned_data['fecha']    
    
    tratamiento = Tratamiento.objects.filter(nombre=nombreTratamiento)[:1]
    
    cliente = Cliente.objects.filter(usuario=usuario)[:1]

    turno = Turno.objects.filter(cliente=cliente).filter(tratamiento=tratamiento).filter(fecha=datosfecha)
    
    if not turno:
        turnoRegistrado = registrarTurno(tratamiento,datosfecha, cliente)
        
        return turnoRegistrado
    else:
        return NULL
    
def registrarTurno(tratamiento,fecha, cliente):
    
    tratamiento = Tratamiento.objects.get(id=tratamiento)
    cliente = Cliente.objects.get(id=cliente)
    
    turno = Turno(cliente=cliente, tratamiento=tratamiento, fecha=fecha)
    
    turno.save()
    
    return turno

def equipos(request):
    fecha = datetime.datetime.now()
   
    equipos = Equipo.objects.all()
    
    recargos = PrecioPorUso.objects.all()

    return render(request, 'equipos_general.html', {'fecha': fecha, 'equipos':equipos, 'recargos':recargos})

@login_required 
@user_passes_test(not_in_tecnicos_group, login_url='/home/')
def home_tecnico(request):
    fecha = datetime.datetime.now()
    usuario = request.user.username
    return render(request, 'home_tecnico.html', {'fecha': fecha, 'usuario':usuario})

@login_required 
@user_passes_test(not_in_clientes_group, login_url='/home/')
def home_cliente(request):
    fecha = datetime.datetime.now()
    usuario = request.user.username
    return render(request, 'home_duenio.html', {'fecha': fecha, 'usuario':usuario})

@login_required 
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def home_duenio(request):
    fecha = datetime.datetime.now()
    usuario = request.user.username
    return render(request, 'home_duenio.html', {'fecha': fecha, 'usuario':usuario})

def tratamientos(request):
    fecha = datetime.datetime.now()
    
    equipos = EquipoTratamiento.objects.all()
    tratamientos = Tratamiento.objects.all()
    
    return render(request, 'tratamientos_general.html', {'fecha': fecha, 'tratamientos': tratamientos, 'equipos':equipos})

@login_required 
@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
def tratamientos_duenio(request):
    fecha = datetime.datetime.now()
    return render(request, 'tratamientos_duenio.html', {'fecha': fecha})

def calendario(request):
    fecha = datetime.datetime.now()
    return render(request, 'fechas_disponibles.html', {'fecha': fecha})


