from django.utils import timezone
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from mejorascgm.models import Mejoracgm
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import csv
import openpyxl
from django.http import HttpResponse




@login_required(login_url='/login/')
def crear_mejora(request):
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"
    fecha_hora_mejora = timezone.now()

    if request.method == "POST":
        servicio = request.POST.get("servicio", "")
        herramienta_de_monitoreo = request.POST.get("herramienta_de_monitoreo", "")
        tipo_de_mejora = request.POST.get("tipo_de_mejora", "")
        numero_peticion = request.POST.get("numero_peticion", "").strip()
        numero_wo = request.POST.get("numero_wo", "").strip()
        servidor = request.POST.get("servidor", "")
        variable = request.POST.get("variable", "")
        peticion_reincidente = request.POST.get("peticion_reincidente", "")
        peticion_anterior = request.POST.get("peticion_anterior", "")
        observaciones = request.POST.get("observaciones", "")
        fecha_hora_mejora_str = request.POST.get("fecha_hora_mejora", "")
        area_responsable = request.POST.get("area_responsable", "")
        mejora_creada_por = request.POST.get("mejora_creada_por", first_name)
        estado = request.POST.get("estado", "Pendiente")
        solucion = request.POST.get("solucion", "")

        # Convertir la fecha si está presente
        if fecha_hora_mejora_str:
            try:
                fecha_hora_mejora = datetime.strptime(fecha_hora_mejora_str, "%Y-%m-%dT%H:%M")
                fecha_hora_mejora = datetime.strptime(fecha_hora_mejora_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                messages.error(request, "Formato de fecha/hora inválido")
                return render(request, "crear_mejora.html", {"first_name": first_name, "fecha_hora_mejora": fecha_hora_mejora})

        # Crear la mejora
        mejora = Mejoracgm.objects.create(
            servicio=servicio,
            herramienta_de_monitoreo=herramienta_de_monitoreo,
            tipo_de_mejora=tipo_de_mejora,
            numero_peticion=numero_peticion,
            numero_wo=numero_wo,
            servidor=servidor,
            variable=variable,
            peticion_reincidente=peticion_reincidente,
            peticion_anterior=peticion_anterior,
            observaciones=observaciones,
            fecha_hora_mejora=fecha_hora_mejora,
            area_responsable=area_responsable,
            mejora_creada_por=mejora_creada_por,
            estado=estado,
            solucion=solucion,
        )

        messages.success(request, f'Se ha creado la mejora "{mejora.servicio}" asociada a la WO {mejora.numero_wo}')
        return redirect("listar_mejora")

    return render(request, "crear_mejora.html", {"first_name": first_name, "fecha_hora_mejora": fecha_hora_mejora})





################################# listar mejora #######################################



@login_required(login_url='/login/')
def listar_mejora(request):
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"
    query = request.GET.get('q', '')

    # Filtrar solo las mejoras con estado "Abierto"
    mejora = Mejoracgm.objects.filter(
        estado="abierto"  # Filtra solo las mejoras abiertas
    ).filter(
        Q(servicio__icontains=query) |
        Q(herramienta_de_monitoreo__icontains=query) |
        Q(tipo_de_mejora__icontains=query) |
        Q(numero_peticion__icontains=query) |
        Q(numero_wo__icontains=query) |
        Q(servidor__icontains=query) |
        Q(variable__icontains=query) |
        Q(peticion_reincidente__icontains=query) |
        Q(peticion_anterior__icontains=query) |
        Q(observaciones__icontains=query) |
        Q(fecha_hora_mejora__icontains=query) |
        Q(area_responsable__icontains=query) |
        Q(mejora_creada_por__icontains=query) |
        Q(estado__icontains=query) |
        Q(solucion__icontains=query) 
    ).order_by('-fecha_hora_mejora')

    paginator = Paginator(mejora, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "listar_mejora.html", {"page_obj": page_obj, "query": query, "first_name": first_name})





################################# listar mejora cerradas  #######################################



@login_required(login_url='/login/')
def listar_mejoras_cerradas(request):
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"
    query = request.GET.get('q', '')

    # Filtrar solo las mejoras con estado "Abierto"
    mejora = Mejoracgm.objects.filter(
        estado="cerrado"  # Filtra solo las mejoras abiertas
    ).filter(
        Q(servicio__icontains=query) |
        Q(herramienta_de_monitoreo__icontains=query) |
        Q(tipo_de_mejora__icontains=query) |
        Q(numero_peticion__icontains=query) |
        Q(numero_wo__icontains=query) |
        Q(servidor__icontains=query) |
        Q(variable__icontains=query) |
        Q(peticion_reincidente__icontains=query) |
        Q(peticion_anterior__icontains=query) |
        Q(observaciones__icontains=query) |
        Q(fecha_hora_mejora__icontains=query) |
        Q(area_responsable__icontains=query) |
        Q(mejora_creada_por__icontains=query) |
        Q(estado__icontains=query) |
        Q(solucion__icontains=query) 
    ).order_by('-fecha_hora_mejora')

    paginator = Paginator(mejora, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "listar_mejoras_cerradas.html", {"page_obj": page_obj, "query": query, "first_name": first_name})




##################################################### Editar mejora ##################################################################3



@login_required(login_url='/login/')
def editar_mejora(request, id):
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"
    mejora = get_object_or_404(Mejoracgm, id=id)

  # Obtener la fecha y hora actuales en formato compatible con <input type="datetime-local">
    fecha_hora_actual = datetime.now().strftime('%Y-%m-%dT%H:%M')
    fecha_hora_actual_aware = datetime.now()  # No es necesario usar timezone.localtime()

    if request.method == 'POST':
        # Actualizar los valores del objeto `Mejoracgm`
        mejora.servicio = request.POST.get('servicio')
        mejora.herramienta_de_monitoreo = request.POST.get('herramienta_de_monitoreo')
        mejora.tipo_de_mejora = request.POST.get('tipo_de_mejora')
        mejora.numero_peticion = request.POST.get('numero_peticion')
        mejora.numero_wo = request.POST.get('numero_wo')
        mejora.servidor = request.POST.get('servidor')
        mejora.variable = request.POST.get('variable')
        mejora.peticion_reincidente = request.POST.get('peticion_reincidente')
        mejora.peticion_anterior = request.POST.get('peticion_anterior')
        mejora.observaciones = request.POST.get('observaciones')

        mejora.fecha_hora_mejora = request.POST.get('fecha_hora_mejora') or fecha_hora_actual_aware
        mejora.fecha_hora_mejora = request.POST.get('fecha_hora_mejora') or fecha_hora_actual

        mejora.area_responsable = request.POST.get('area_responsable')
        mejora.mejora_creada_por = request.POST.get('mejora_creada_por')

        # Actualizar los valores del objeto `Estadomejora`
        mejora.estado = request.POST.get('estado')
        mejora.solucion = request.POST.get('solucion')

        # Si el campo de fecha está vacío, usa la fecha actual
        mejora.fecha_hora = request.POST.get('fecha_hora') or fecha_hora_actual

        # Guardar los cambios en ambas tablas
        mejora.save()
       

        # Mensaje de éxito
        messages.success(request, f'Se ha editado correctamente la mejora con el servicio {mejora.servicio} y el número WO {mejora.numero_wo}.')

        return redirect('listar_mejora')

    return render(request, 'editar_mejora.html', {
        'mejora': mejora,
        'first_name': first_name, 
        'fecha_hora_actual': fecha_hora_actual
    })

###################################enviar email ########################################


@login_required(login_url='/login/')
def enviar_mejora_email(request, mejora_id):
    # Obtener la gestión editada
    mejora = get_object_or_404(Mejoracgm, id=mejora_id)

    # Renderizar la tabla como HTML solo con esta gestión
    contenido_html = render_to_string('email_template_mejora.html', {'mejoras': [mejora]})

    # Configurar el correo
    subject = "Solicitud de mejora"
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
    
    
    
    
    ############################## descargar mejoras ######################################


@login_required(login_url='/login/')
def descargar_mejora(request):
        # Obtener los IDs seleccionados desde el formulario
        ids_seleccionados = request.GET.getlist("mejoras")

        # Filtrar las gestiones seleccionadas
        mejoras = Mejoracgm.objects.filter(id__in=ids_seleccionados)

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
                "ID", "Servicio", "Herramienta de Monitoreo", "Tipo de Mejora", "Número de Petición",
                "Número WO", "Servidor", "Variable", "Petición Reincidente", "Petición Anterior",
                "Observaciones", "Fecha y Hora de Mejora", "Área Responsable", "Mejora Creada Por",
                "Estado", "Solución"
            ])

            # Escribir datos de las gestiones seleccionadas
            for mejora in mejoras:
                writer.writerow([
                    mejora.id,
                    mejora.servicio,
                    mejora.herramienta_de_monitoreo,
                    mejora.tipo_de_mejora,
                    mejora.numero_peticion,
                    mejora.numero_wo,
                    mejora.servidor,
                    mejora.variable,
                    mejora.peticion_reincidente,
                    mejora.peticion_anterior,
                    mejora.observaciones,
                    mejora.fecha_hora_mejora,
                    mejora.area_responsable,
                    mejora.mejora_creada_por,
                    mejora.estado,
                    mejora.solucion
                ])

            return response

        elif formato == 'xlsx':
            # Crear la respuesta con XLSX
            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = 'attachment; filename="gestiones_seleccionadas.xlsx"'

            # Crear un libro de trabajo y una hoja
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Mejoras"

            # Escribir encabezados
            ws.append([
                "ID", "Servicio", "Herramienta de Monitoreo", "Tipo de Mejora", "Número de Petición",
                "Número WO", "Servidor", "Variable", "Petición Reincidente", "Petición Anterior",
                "Observaciones", "Fecha y Hora de Mejora", "Área Responsable", "Mejora Creada Por",
                "Estado", "Solución"
            ])

            # Escribir datos de las gestiones seleccionadas
            for mejora in mejoras:
                ws.append([
                    mejora.id,
                    mejora.servicio,
                    mejora.herramienta_de_monitoreo,
                    mejora.tipo_de_mejora,
                    mejora.numero_peticion,
                    mejora.numero_wo,
                    mejora.servidor,
                    mejora.variable,
                    mejora.peticion_reincidente,
                    mejora.peticion_anterior,
                    mejora.observaciones,
                    mejora.fecha_hora_mejora,
                    mejora.area_responsable,
                    mejora.mejora_creada_por,
                    mejora.estado,
                    mejora.solucion
                ])

            # Guardar el archivo en la respuesta
            wb.save(response)

            return response

        else:
            # Si el formato no es válido, devolver un error
            messages.error(request, "Formato no soportado")
            return redirect('listar_mejora')
