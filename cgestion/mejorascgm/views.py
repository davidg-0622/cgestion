from django.utils import timezone
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from mejorascgm.models import Mejoracgm
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q






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
                fecha_hora_mejora = timezone.make_aware(fecha_hora_mejora)
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




def editar_mejora(request, id):
    first_name = request.user.first_name if request.user.is_authenticated else "Invitado"
    mejora = get_object_or_404(Mejoracgm, id=id)

  

    # Obtener la fecha y hora actuales en formato compatible con <input type="datetime-local>
    fecha_hora_actual = timezone.localtime().strftime('%Y-%m-%dT%H:%M')
    fecha_hora_actual_aware = timezone.localtime()

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

