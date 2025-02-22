from django.shortcuts import render, get_object_or_404
from gestiones.models import Gestion, Servicio
from django.contrib.auth.forms import UserCreationForm
from gestiones.forms import RegisterForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.db.models import Q
import csv
import openpyxl
from django.http import HttpResponse




############################## Crear gestion #######################################


def creargestion(request):
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"
    
    fecha_hora_mejora = timezone.now()  # Obtiene la fecha y hora actual

    if request.method == "POST":
        # Obtener datos del formulario
        servicio = request.POST.get("servicio") or None
        tipo_de_gestion = request.POST.get("tipo_de_gestion")or None
        numero_caso = request.POST.get("numero_caso") or None
        detectada_por = request.POST.get("detectada_por") or None
        causado_por_certificado_digital = request.POST.get("causado_por_certificado_digital") == "on"
        incidente_generado_por_OC = request.POST.get("incidente_generado_por_OC") == "on" 
        atribuible_a = request.POST.get("atribuible_a") or None
        tipo_de_falla = request.POST.get("tipo_de_falla")or None
        detalle = request.POST.get("detalle")
        tipo_causa = request.POST.get("tipo_causa") or None
        causa = request.POST.get("causa")
        validaciones = request.POST.get("validaciones")
        solucion = request.POST.get("solucion")
        responsable_gioti = request.POST.get("responsable_gioti")
        fecha_hora_inicial = request.POST.get("fecha_hora_inicial") or timezone.now()  # Si no se envía, usa la fecha actual
        fecha_hora_final = request.POST.get("fecha_hora_final") or None
        postular_amg = request.POST.get("postular_amg") == "on"
        gioti = request.POST.get("gioti") == "on"

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

    return render(request, "crear_gestion.html", {"first_name": first_name, "fecha_hora_mejora": fecha_hora_mejora})




################################# listar gestion #######################################



def listar_gestiones(request):
    # Obtener el nombre del usuario autenticado (o "Invitado" si no está autenticado)
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"
    
    # Obtener los parámetros GET
    query = request.GET.get('q', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin') 

    # Obtener todas las gestiones
    gestiones = Gestion.objects.all()

    # Filtrar por término de búsqueda si existe
    if query:
        gestiones = gestiones.filter(
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
            Q(responsable_gioti__icontains=query) |
            Q(fecha_hora_inicial__icontains=query) |
            Q(fecha_hora_final__icontains=query)
        )

    # Convertir las fechas a datetime y filtrar por fechas si están presentes
    if fecha_inicio:
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        gestiones = gestiones.filter(fecha_hora_inicial__gte=fecha_inicio)
    
    if fecha_fin:
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d") + timedelta(days=1)
        gestiones = gestiones.filter(fecha_hora_final__lt=fecha_fin)

    # Configurar la paginación (10 registros por página)
    paginator = Paginator(gestiones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizar la plantilla con los datos
    return render(request, "listar_gestiones.html", {
        "page_obj": page_obj,
        "query": query,
        "first_name": first_name,
        "fecha_inicio": request.GET.get('fecha_inicio', ''),  # Mantiene el valor en la vista
        "fecha_fin": request.GET.get('fecha_fin', '')  # Mantiene el valor en la vista
    })




############################# Editar gestion ###########################################

def editar_gestion(request, id):
    # Obtener el nombre del usuario autenticado (o "Invitado" si no está autenticado)
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"
    # Obtiene la instancia de la gestión a editar
    gestion = get_object_or_404(Gestion, id=id)
    
    # Obtener la fecha y hora actuales
    fecha_hora_actual = datetime.now().strftime('%Y-%m-%dT%H:%M')

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
        fecha_hora_final = request.POST.get('fecha_hora_final') or None 
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

    return render(request, 'editar_gestion.html', {'gestion': gestion, "first_name":first_name,'fecha_hora_actual': fecha_hora_actual})


#################



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

##############################funcion de login ####################################

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


##################funcion de logout###################################

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige a la página de login (ajústala según tu URL)



##########################enviar email #########################################

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from .models import Gestion

def enviar_gestion_email(request, gestion_id):
    # Obtener la gestión editada
    gestion = get_object_or_404(Gestion, id=gestion_id)

    # Renderizar la tabla como HTML solo con esta gestión
    contenido_html = render_to_string('email_template.html', {'gestiones': [gestion]})

    # Configurar el correo
    subject = "Reporte de Gestion"
    from_email = "davidg06.buitrago@gmail.com"
    recipient_list = ["davidg06.buitrago@gmail.com"]  

    # Crear el correo con contenido HTML
    email = EmailMessage(subject, contenido_html, from_email, recipient_list)
    email.content_subtype = "html"  

    try:
        email.send()
        return render(request, 'success.html', {'mensaje': 'Correo enviado correctamente'})
    except Exception as e:
        return render(request, 'error.html', {'mensaje': f'Error al enviar correo: {str(e)}'})



##############################descagar gestiones ######################################


def descargar_gestiones(request):
    # Obtener los IDs seleccionados desde el formulario
    ids_seleccionados = request.GET.getlist("gestiones")

    # Filtrar las gestiones seleccionadas
    gestiones = Gestion.objects.filter(id__in=ids_seleccionados)
    
    # Obtener el formato deseado desde la URL, por defecto CSV
    formato = request.GET.get('formato', 'csv')
    
    if formato == 'csv':
        # Crear la respuesta con CSV
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="gestiones_seleccionadas.csv"'

        # Crear un escritor CSV
        writer = csv.writer(response)
        
        # Escribir encabezados
        writer.writerow([
            "ID", "Servicio", "Tipo de Gestión", "Número de Caso", "Detectada Por",
            "Causado por Certificado Digital", "Incidente Generado por OC", "Atribuible A",
            "Tipo de Falla", "Detalle", "Tipo de Causa", "Causa", "Validaciones",
            "Solución", "Responsable GIOTI", "Fecha Hora Inicial", "Fecha Hora Final",
            "Postular AMG", "GIOTI"
        ])
        
        # Escribir datos de las gestiones seleccionadas
        for gestion in gestiones:
            # Eliminar la zona horaria si está presente
            fecha_hora_inicial = gestion.fecha_hora_inicial.replace(tzinfo=None) if gestion.fecha_hora_inicial else None
            fecha_hora_final = gestion.fecha_hora_final.replace(tzinfo=None) if gestion.fecha_hora_final else None
            
            writer.writerow([
                gestion.id,
                gestion.servicio,
                gestion.tipo_de_gestion,
                gestion.numero_caso,
                gestion.detectada_por,
                gestion.causado_por_certificado_digital,
                gestion.incidente_generado_por_OC,
                gestion.atribuible_a,
                gestion.tipo_de_falla,
                gestion.detalle,
                gestion.tipo_causa,
                gestion.causa,
                gestion.validaciones,
                gestion.solucion,
                gestion.responsable_gioti,
                fecha_hora_inicial,
                fecha_hora_final,
                gestion.postular_amg,
                gestion.gioti
            ])
        
    elif formato == 'xlsx':
        # Crear la respuesta con XLSX
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="gestiones_seleccionadas.xlsx"'

        # Crear un libro de trabajo y una hoja
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Gestiones"

        # Escribir encabezados
        ws.append([
            "ID", "Servicio", "Tipo de Gestión", "Número de Caso", "Detectada Por",
            "Causado por Certificado Digital", "Incidente Generado por OC", "Atribuible A",
            "Tipo de Falla", "Detalle", "Tipo de Causa", "Causa", "Validaciones",
            "Solución", "Responsable GIOTI", "Fecha Hora Inicial", "Fecha Hora Final",
            "Postular AMG", "GIOTI"
        ])

        # Escribir datos de las gestiones seleccionadas
        for gestion in gestiones:
            # Eliminar la zona horaria si está presente
            fecha_hora_inicial = gestion.fecha_hora_inicial.replace(tzinfo=None) if gestion.fecha_hora_inicial else None
            fecha_hora_final = gestion.fecha_hora_final.replace(tzinfo=None) if gestion.fecha_hora_final else None
            
            ws.append([
                gestion.id,
                gestion.servicio,
                gestion.tipo_de_gestion,
                gestion.numero_caso,
                gestion.detectada_por,
                gestion.causado_por_certificado_digital,
                gestion.incidente_generado_por_OC,
                gestion.atribuible_a,
                gestion.tipo_de_falla,
                gestion.detalle,
                gestion.tipo_causa,
                gestion.causa,
                gestion.validaciones,
                gestion.solucion,
                gestion.responsable_gioti,
                fecha_hora_inicial,
                fecha_hora_final,
                gestion.postular_amg,
                gestion.gioti
            ])

        # Guardar el archivo en la respuesta
        wb.save(response)

    return response





#############################Listar casos en investigacion #################################

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Gestion

def listar_gestiones_en_investigacion(request):
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"
    query = request.GET.get('q', '')


    # Construcción del filtro
    gestion = Gestion.objects.filter(tipo_causa="En investigacion").filter(
        Q(servicio__icontains=query) |
        Q(tipo_de_gestion__icontains=query) |
        Q(numero_caso__icontains=query) |
        Q(detectada_por__icontains=query) |
        Q(causado_por_certificado_digital__icontains=query) |
        Q(incidente_generado_por_OC__icontains=query) |
        Q(atribuible_a__icontains=query) |
        Q(tipo_de_falla__icontains=query) |
        Q(detalle__icontains=query) |
        Q(tipo_causa__icontains=query) |
        Q(causa__icontains=query) |
        Q(validaciones__icontains=query) |
        Q(solucion__icontains=query) |
        Q(responsable_gioti=query) |
        Q(fecha_hora_inicial__icontains=query) |
        Q(fecha_hora_final__icontains=query)
    )

    gestion = gestion.order_by('-fecha_hora_inicial')

    # Paginación
    paginator = Paginator(gestion, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "listar_gestiones_investigacion.html", {
        "page_obj": page_obj,
        "query": query,
        "first_name": first_name
    })


#######################crear grafico con la data gestion ##########################
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from django.http import HttpResponse
from django.db.models import Count
from .models import Gestion

def grafico_gestiones(request):
    # Obtener los datos agrupados por responsable_gioti
    gestiones = Gestion.objects.values('responsable_gioti').annotate(total_casos=Count('numero_caso'))

    # Convertir a DataFrame
    df = pd.DataFrame(list(gestiones))

    # Verificar si hay datos
    if df.empty:
        return HttpResponse("No hay datos para mostrar el gráfico.")

    # Crear el gráfico
    plt.figure(figsize=(10, 5))
    sns.barplot(x='responsable_gioti', y='total_casos', data=df, palette='Blues_r')
    plt.title('Cantidad de Casos por Responsable GIOTI')
    plt.xlabel('Responsable GIOTI')
    plt.ylabel('Número de Casos')
    plt.xticks(rotation=45)

    # Guardar el gráfico en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la imagen a base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return HttpResponse(f'<img src="data:image/png;base64,{image_base64}" />')


