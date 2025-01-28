from django.shortcuts import render, get_object_or_404

from gestiones.models import Gestion, Servicio
from django.contrib.auth.forms import UserCreationForm
from gestiones.forms import RegisterForm



############################## Crear gestion #######################################

from django.shortcuts import render, redirect
from gestiones.models import Gestion
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render

def creargestion(request):
    if request.method == "POST":
        # Obtener datos del formulario
        servicio = request.POST.get("servicio")
        tipo_de_gestion = request.POST.get("tipo_de_gestion")
        numero_caso = request.POST.get("numero_caso")
        detectada_por = request.POST.get("detectada_por")
        causado_por_certificado_digital = request.POST.get("causado_por_certificado_digital")== "on"
        incidente_generado_por_OC = request.POST.get("incidente_generado_por_OC") == "on"
        atribuible_a = request.POST.get("atribuible_a")
        tipo_de_falla = request.POST.get("tipo_de_falla")
        detalle = request.POST.get("detalle")
        tipo_causa = request.POST.get("tipo_causa")
        causa = request.POST.get("causa")
        validaciones = request.POST.get("validaciones")
        solucion = request.POST.get("solucion")
        responsable_gioti = request.POST.get("responsable_gioti")
        fecha_hora_inicial = request.POST.get("fecha_hora_inicial")
        fecha_hora_final = request.POST.get("fecha_hora_final")
        postular_amg = request.POST.get("postular_amg") == "on"
        gioti = request.POST.get("gioti")== "on"

        # Crear el objeto Gestión
        gestion = Gestion(
            servicio=servicio,
            tipo_de_gestion=tipo_de_gestion,
            numero_caso=numero_caso,
            detectada_por=detectada_por,
            causado_por_certificado_digital=causado_por_certificado_digital,
            incidente_generado_por_OC=incidente_generado_por_OC,
            atribuible_a=atribuible_a,
            tipo_de_falla=tipo_de_falla,
            detalle=detalle,
            tipo_causa=tipo_causa,
            causa=causa,
            validaciones=validaciones,
            solucion=solucion,
            responsable_gioti=responsable_gioti,
            fecha_hora_inicial=fecha_hora_inicial,
            fecha_hora_final=fecha_hora_final,
            postular_amg=postular_amg,
            gioti=gioti,
        )
        gestion.save()
        messages.success(request, f'Se ha creado correctamente la gestión con el incidente {gestion.numero_caso} y el servicio {gestion.servicio}.')

        return redirect("/")  # Redirigir a una página de listado o detalle

    return render(request, "crear_gestion.html")



################################# listar gestion #######################################



from django.db.models import Q



def listar_gestiones(request):
    # Obtener el término de búsqueda desde los parámetros GET
    query = request.GET.get('q', '')

    # Filtrar las gestiones basadas en el término de búsqueda
    gestiones = Gestion.objects.filter(
        Q(numero_caso__icontains=query) |
        Q(detalle__icontains=query) |
        Q(solucion__icontains=query) |
        Q(servicio__icontains=query) |
        Q(tipo_de_gestion__icontains=query) |
        Q(detectada_por__icontains=query) |
        Q(causado_por_certificado_digital__icontains=query) |
        Q(incidente_generado_por_OC__icontains=query) |
        Q(atribuible_a__icontains=query) |
        Q(tipo_de_falla__icontains=query) |
        Q(tipo_causa__icontains=query) |
        Q(causa__icontains=query) |
        Q(validaciones__icontains=query) |
        Q(responsable_gioti__icontains=query)
    ).order_by('-id')

    # Configurar el paginador (10 registros por página)
    paginator = Paginator(gestiones, 10)

    # Obtener el número de página actual desde los parámetros GET
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pasar las gestiones paginadas y el término de búsqueda al contexto
    return render(request, "listar_gestiones.html", {"page_obj": page_obj, "query": query})







############################# Editar gestion ###########################################

def editar_gestion(request, id):
    # Obtiene la instancia de la gestión a editar
    gestion = get_object_or_404(Gestion, id=id)

    if request.method == 'POST':
        # Procesa los campos del formulario
        servicio = request.POST.get('servicio')
        tipo_de_gestion = request.POST.get('tipo_de_gestion')
        numero_caso = request.POST.get('numero_caso')
        detectada_por = request.POST.get('detectada_por')
        causado_por_certificado_digital = 'causado_por_certificado_digital' in request.POST
        incidente_generado_por_OC = 'incidente_generado_por_OC' in request.POST
        atribuible_a = request.POST.get('atribuible_a')
        tipo_de_falla = request.POST.get('tipo_de_falla')
        detalle = request.POST.get('detalle')
        tipo_causa = request.POST.get('tipo_causa')
        causa = request.POST.get('causa')
        validaciones = request.POST.get('validaciones')
        solucion = request.POST.get('solucion')
        responsable_gioti = request.POST.get('responsable_gioti')
        fecha_hora_inicial = request.POST.get('fecha_hora_inicial')
        fecha_hora_final = request.POST.get('fecha_hora_final')
        postular_amg = 'postular_amg' in request.POST
        gioti = 'gioti' in request.POST

        # Actualiza la instancia de la gestión con los nuevos valores
        gestion.servicio = servicio
        gestion.tipo_de_gestion = tipo_de_gestion
        gestion.numero_caso = numero_caso
        gestion.detectada_por = detectada_por
        gestion.causado_por_certificado_digital = causado_por_certificado_digital
        gestion.incidente_generado_por_OC = incidente_generado_por_OC
        gestion.atribuible_a = atribuible_a
        gestion.tipo_de_falla = tipo_de_falla
        gestion.detalle = detalle
        gestion.tipo_causa = tipo_causa
        gestion.causa = causa
        gestion.validaciones = validaciones
        gestion.solucion = solucion
        gestion.responsable_gioti = responsable_gioti
        gestion.fecha_hora_inicial = fecha_hora_inicial
        gestion.fecha_hora_final = fecha_hora_final
        gestion.postular_amg = postular_amg
        gestion.gioti = gioti

        # Guarda los cambios en la base de datos
        gestion.save()
        
        #Crear mensaje flas (sesion que solo se muestra una vez)
        # Crear mensaje flash (sesión que solo se muestra una vez)
        # Crear mensaje flash (sesión que solo se muestra una vez)
        messages.success(request, f'Se ha editado correctamente la gestión con el incidente {gestion.numero_caso} y el servicio {gestion.servicio}.')


        
        # Redirige a la página de gestiones
        return redirect('listar_gestiones')  # Asume que 'listar_gestiones' es el nombre de la URL de gestiones.html

    return render(request, 'editar_gestion.html', {
        'gestion': gestion,
    })





from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register_page(request):
    # Crea el formulario de registro
    register_form = RegisterForm()
    
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        
        if register_form.is_valid():
            register_form.save()
            # Redirigir a la página de gestión o la URL correcta
            return redirect('login')  # Asegúrate de que 'listar_gestiones' sea el nombre de la URL definida en tus urls.py
    
    return render(request, 'users/register.html', {'register_form': register_form})




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('listar_gestiones')  # Redirige al usuario después de iniciar sesión
        else:
            messages.error(request, 'Credenciales incorrectas. Inténtalo nuevamente.')
    
    return render(request, 'users/login.html', {'title': 'Login'})



def inicio(request):
    return render(request, 'gestiones.html')


