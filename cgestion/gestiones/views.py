from .models import Gestion
from django.db.models import Count
import base64
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, localtime
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .forms import ChangePasswordForm
from django.contrib import admin


############################## Crear gestion #######################################

@login_required(login_url='/login/')
def creargestion(request):
     # Obtener el nombre del usuario autenticado (o "Invitado" si no está autenticado)
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"
    last_name = request.user.last_name if request.user.is_authenticated else ""

    fecha_hora_mejora = timezone.now()  # Obtiene la fecha y hora actual

    if request.method == "POST":
        # Obtener datos del formulario
        servicio = request.POST.get("servicio") or None
        tipo_de_gestion = request.POST.get("tipo_de_gestion") or None
        numero_caso = request.POST.get("numero_caso") or None
        detectada_por = request.POST.get("detectada_por") or None
        causado_por_certificado_digital = request.POST.get(
            "causado_por_certificado_digital") == "on"
        incidente_generado_por_OC = request.POST.get(
            "incidente_generado_por_OC") == "on"
        atribuible_a = request.POST.get("atribuible_a") or None
        tipo_de_falla = request.POST.get("tipo_de_falla") or None
        detalle = request.POST.get("detalle")
        tipo_causa = request.POST.get("tipo_causa") or None
        causa = request.POST.get("causa")
        validaciones = request.POST.get("validaciones")
        solucion = request.POST.get("solucion")
        responsable_gioti = request.POST.get("responsable_gioti")
        # Si no se envía, usa la fecha actual
        fecha_hora_inicial = request.POST.get(
            "fecha_hora_inicial") or timezone.now()
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
        messages.success(
            request, f'Se ha creado correctamente la gestión con el incidente {gestion.numero_caso} y el servicio {gestion.servicio}.')

        return redirect("/")  # Redirigir a una página de listado o detalle

    return render(request, "crear_gestion.html", {"first_name": first_name, "last_name": last_name, "fecha_hora_mejora": fecha_hora_mejora})


################################# listar gestion #######################################
@login_required(login_url='/login/')
def listar_gestiones(request):

    # Obtener el nombre del usuario autenticado (o "Invitado" si no está autenticado)
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"

    # Obtener los parámetros GET
    query = request.GET.get('q', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Obtener todas las gestiones
    gestiones = Gestion.objects.all().order_by('-fecha_hora_inicial')

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
        fecha_fin = datetime.strptime(
            fecha_fin, "%Y-%m-%d") + timedelta(days=1)
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
        # Mantiene el valor en la vista
        "fecha_inicio": request.GET.get('fecha_inicio', ''),
        # Mantiene el valor en la vista
        "fecha_fin": request.GET.get('fecha_fin', '')
    })


############################# Editar gestion ###########################################
@login_required(login_url='/login/')
def editar_gestion(request, id):
    # Obtener el nombre del usuario autenticado (o "Invitado" si no está autenticado)
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"
    last_name = request.user.last_name if request.user.is_authenticated else ""

    # Verificar si la gestión ya existe
    gestion = Gestion.objects.filter(id=id).first()
    if not gestion:
        # Si no existe, obtener la instancia de la gestión a editar
        gestion = get_object_or_404(Gestion, id=id)

    # Verificar si el usuario ya está en responsable_gioti
    if gestion.responsable_gioti and first_name not in gestion.responsable_gioti:
        responsable_gioti = f"{gestion.responsable_gioti} -- {first_name} {last_name}"
    else:
        responsable_gioti = gestion.responsable_gioti  # No lo repite

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

        # Crear mensaje flash
        messages.success(
            request, f'Se ha editado correctamente la gestión con el incidente {gestion.numero_caso} y el servicio {gestion.servicio}.'
        )

        # Redirige a la página de gestiones
        return redirect('listar_gestiones')

    return render(request, 'editar_gestion.html', {
        'gestion': gestion,
        "first_name": first_name,
        'fecha_hora_actual': fecha_hora_actual,
        'responsable_gioti': responsable_gioti
    })


#################

def register_page(request):
    register_form = RegisterForm()

    if request.method == "POST":
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            email = register_form.cleaned_data.get('email').strip().lower()
            username = register_form.cleaned_data.get('username').strip().lower()

            if not email.endswith('@bancolombia.com.co'):
                messages.error(request, 'El correo solo está permitido con dominio Bancolombia (@bancolombia.com.co)')
                return render(request, 'users/register.html', {'register_form': register_form})

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Este nombre de usuario ya está registrado.')
                return render(request, 'users/register.html', {'register_form': register_form})

            user = register_form.save(commit=False)  # No guarda aún
            user.username = username  # Forzar minúsculas
            user.date_joined = now()  # Guarda la fecha con la zona horaria correcta
            user.save()  # Guardar usuario

            messages.success(request, 'Registro exitoso. Por favor, inicie sesión.')
            return redirect('login')

        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')

    return render(request, 'users/register.html', {'register_form': register_form})






############################## funcion de login ####################################


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username').lower()  # Convertir a minúsculas
        password = request.POST.get('password')

        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirige al usuario después de iniciar sesión
            return redirect('listar_gestiones')
        else:
            messages.error(
                request, 'Credenciales incorrectas. Inténtalo nuevamente.')

    return render(request, 'users/login.html', {'title': 'Login'})


################## funcion de logout###################################

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    # Redirige a la página de login (ajústala según tu URL)
    return redirect('login')


########################## enviar email #########################################

@login_required(login_url='/login/')
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


############################## descagar gestiones ######################################

@login_required(login_url='/login/')
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
            fecha_hora_inicial = gestion.fecha_hora_inicial.replace(
                tzinfo=None) if gestion.fecha_hora_inicial else None
            fecha_hora_final = gestion.fecha_hora_final.replace(
                tzinfo=None) if gestion.fecha_hora_final else None

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
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
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
            fecha_hora_inicial = gestion.fecha_hora_inicial.replace(
                tzinfo=None) if gestion.fecha_hora_inicial else None
            fecha_hora_final = gestion.fecha_hora_final.replace(
                tzinfo=None) if gestion.fecha_hora_final else None

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


############################# Listar casos en investigacion #################################

@login_required(login_url='/login/')
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



################################Cambiar contraseña ##################################


@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantiene la sesión activa
            messages.success(request, "Tu contraseña ha sido cambiada exitosamente.")
            return redirect("login")  # Redirige a la vista del perfil o donde prefieras
    else:
        form = ChangePasswordForm(user=request.user)
    
    return render(request, "users/change_password.html", {"form": form})





def perfil(request):
    return render(request, "users/login.html")


########################Descargar desde el panel de administrador ####################



class TuModeloAdmin(admin.ModelAdmin):
    list_display = ("servicio", "tipo_de_gestion", "numero_caso", 'detectada_por', 'causado_por_certificado_digital',
                    'incidente_generado_por_OC', 'atribuible_a', 'tipo_de_falla', 'detalle', 'tipo_causa', 'causa', 'validaciones',
                    'solucion', 'responsable_gioti', 'fecha_hora_inicial', 'fecha_hora_final', 'postular_amg', 'gioti' 
                    )  # Ajusta con los campos de tu modelo
    actions = ["exportar_csv"]

    def exportar_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="datos.csv"'
        
        writer = csv.writer(response)
        writer.writerow(["ID", "Servicio", "Tipo de Gestión", "Número de Caso", "Detectada Por",
            "Causado por Certificado Digital", "Incidente Generado por OC", "Atribuible A",
            "Tipo de Falla", "Detalle", "Tipo de Causa", "Causa", "Validaciones",
            "Solución", "Responsable GIOTI", "Fecha Hora Inicial", "Fecha Hora Final",
            "Postular AMG", "GIOTI"])  # Encabezados

        for obj in queryset:
            fecha_hora_inicial = obj.fecha_hora_inicial.replace(tzinfo=None) if obj.fecha_hora_inicial else None
            fecha_hora_final = obj.fecha_hora_final.replace(tzinfo=None) if obj.fecha_hora_final else None

            writer.writerow([obj.id,
                obj.servicio,
                obj.tipo_de_gestion,
                obj.numero_caso,
                obj.detectada_por,
                obj.causado_por_certificado_digital,
                obj.incidente_generado_por_OC,
                obj.atribuible_a,
                obj.tipo_de_falla,
                obj.detalle,
                obj.tipo_causa,
                obj.causa,
                obj.validaciones,
                obj.solucion,
                obj.responsable_gioti,
                fecha_hora_inicial,
                fecha_hora_final,
                obj.postular_amg,
                obj.gioti])

        return response
    
    exportar_csv.short_description = "Exportar a CSV"

















############################  Grafico  incidentes Gioti ###############################
from collections import Counter
import io
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Cambiar el backend antes de usar matplotlib
import matplotlib.pyplot as plt
import seaborn as sns 
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from .models import Gestion  # Asegúrate de importar tu modelo
from datetime import datetime, timedelta


def grafico_gestiones(request):
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"

    # Obtener parámetros de fecha desde el formulario y convertirlos a datetime
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    fecha_inicio = fecha_fin = None  # Inicializar fechas

    if fecha_inicio_str and fecha_fin_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
            fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)  # Asegurar que la fecha fin cubra todo el día
        except ValueError:
            fecha_inicio = fecha_fin = None  # En caso de error, evitar filtro inválido

    # Filtro base (solo incidentes)
    filtro = Q(tipo_de_gestion="Incidente") & Q(gioti=True)

    # Aplicar filtro de fechas si están presentes
    if fecha_inicio and fecha_fin:
        filtro &= Q(fecha_hora_inicial__gte=fecha_inicio, fecha_hora_inicial__lte=fecha_fin)

    # Obtener valores filtrados
    gestiones = Gestion.objects.filter(filtro).values_list('responsable_gioti', flat=True)

    # Contador para cada responsable individual
    contador_responsables = Counter()
    for gestion in gestiones:
        if gestion:
            responsables = [r.strip() for r in gestion.split('--')]  
            contador_responsables.update(responsables)

    # Convertir datos en DataFrame
    df = pd.DataFrame(contador_responsables.items(), columns=['responsable_gioti', 'total_casos'])

    # Si no hay datos, agregar una fila con "Sin datos"
    if df.empty:
        df = pd.DataFrame({'responsable_gioti': ['Sin datos'], 'total_casos': [0]})

    # Crear el gráfico
    plt.figure(figsize=(12, 6))
    sns.barplot(x='responsable_gioti', y='total_casos', data=df, palette='viridis')
    plt.title('Cantidad de Casos por Responsable COES', fontsize=12)
    plt.xlabel('Responsable COES', fontsize=10)
    plt.ylabel('Número de Casos', fontsize=10)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()

    # Guardar el gráfico en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la imagen a base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Convertir el DataFrame en una lista de diccionarios
    data = df.to_dict(orient='records')

    return render(request, 'grafico_gestiones.html', {
        'first_name': first_name,
        'image_base64': image_base64,
        'data': data,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str,
    })
    
    
    
    
    #################################Grafica incidentes sin gioti##########################
def grafico_gestiones_no_gioti(request):
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"

    # Obtener parámetros de fecha desde el formulario y convertirlos a datetime
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    fecha_inicio = fecha_fin = None  # Inicializar fechas

    if fecha_inicio_str and fecha_fin_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
            fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)  # Asegurar que la fecha fin cubra todo el día
        except ValueError:
            fecha_inicio = fecha_fin = None  # En caso de error, evitar filtro inválido

    # Filtro base (solo incidentes)
    filtro = Q(tipo_de_gestion="Incidente") & Q(gioti=False)

    # Aplicar filtro de fechas si están presentes
    if fecha_inicio and fecha_fin:
        filtro &= Q(fecha_hora_inicial__gte=fecha_inicio, fecha_hora_inicial__lte=fecha_fin)

    # Obtener valores filtrados
    gestiones = Gestion.objects.filter(filtro).values_list('responsable_gioti', flat=True)

    # Contador para cada responsable individual
    contador_responsables = Counter()
    for gestion in gestiones:
        if gestion:
            responsables = [r.strip() for r in gestion.split('--')]  
            contador_responsables.update(responsables)

    # Convertir datos en DataFrame
    df = pd.DataFrame(contador_responsables.items(), columns=['responsable_gioti', 'total_casos'])

    # Si no hay datos, agregar una fila con "Sin datos"
    if df.empty:
        df = pd.DataFrame({'responsable_gioti': ['Sin datos'], 'total_casos': [0]})

    # Crear el gráfico
    plt.figure(figsize=(12, 6))
    sns.barplot(x='responsable_gioti', y='total_casos', data=df, palette='viridis')
    plt.title('Cantidad de Casos por Responsable COES', fontsize=12)
    plt.xlabel('Responsable COES', fontsize=10)
    plt.ylabel('Número de Casos', fontsize=10)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()

    # Guardar el gráfico en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la imagen a base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Convertir el DataFrame en una lista de diccionarios
    data = df.to_dict(orient='records')

    return render(request, 'grafico_gestiones_no_gioti.html', {
        'first_name': first_name,
        'image_base64': image_base64,
        'data': data,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str,
    })
    
    
    ##############################grafico eventos##################
    
def grafico_gestiones_eventos(request):
    
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"

    # Obtener parámetros de fecha desde el formulario y convertirlos a datetime
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    fecha_inicio = fecha_fin = None  # Inicializar fechas

    if fecha_inicio_str and fecha_fin_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
            fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)  # Asegurar que la fecha fin cubra todo el día
        except ValueError:
            fecha_inicio = fecha_fin = None  # En caso de error, evitar filtro inválido

    # Filtro base (solo incidentes)
    filtro = Q(tipo_de_gestion="Evento")

    # Aplicar filtro de fechas si están presentes
    if fecha_inicio and fecha_fin:
        filtro &= Q(fecha_hora_inicial__gte=fecha_inicio, fecha_hora_inicial__lte=fecha_fin)

    # Obtener valores filtrados
    gestiones = Gestion.objects.filter(filtro).values_list('responsable_gioti', flat=True)

    # Contador para cada responsable individual
    contador_responsables = Counter()
    for gestion in gestiones:
        if gestion:
            responsables = [r.strip() for r in gestion.split('--')]  
            contador_responsables.update(responsables)

    # Convertir datos en DataFrame
    df = pd.DataFrame(contador_responsables.items(), columns=['responsable_gioti', 'total_casos'])

    # Si no hay datos, agregar una fila con "Sin datos"
    if df.empty:
        df = pd.DataFrame({'responsable_gioti': ['Sin datos'], 'total_casos': [0]})

    # Crear el gráfico
    plt.figure(figsize=(12, 6))
    sns.barplot(x='responsable_gioti', y='total_casos', data=df, palette='coolwarm')
    plt.title('Cantidad de Casos por Responsable COES', fontsize=12)
    plt.xlabel('Responsable COES', fontsize=10)
    plt.ylabel('Número de Eventos', fontsize=10)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()

    # Guardar el gráfico en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la imagen a base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Convertir el DataFrame en una lista de diccionarios
    data = df.to_dict(orient='records')

    return render(request, 'grafico_gestiones_eventos.html', {
        'first_name': first_name,
        'image_base64': image_base64,
        'data': data,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str,
    })

