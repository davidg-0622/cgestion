from django.shortcuts import render

from gestiones.models import Gestion, Servicio

### Crear gestion #######

from django.shortcuts import render, redirect
from gestiones.models import Gestion

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
        return redirect("/")  # Redirigir a una página de listado o detalle

    return render(request, "crear_gestion.html")



### listar gestion #######

def listar_gestiones(request):
    # Obtener todas las gestiones
    gestiones = Gestion.objects.all()

    # Pasar las gestiones al contexto para que se muestren en la plantilla
    return render(request, "listar_gestiones.html", {"gestiones": gestiones})



def inicio(request):
    return render(request, 'gestiones.html')


def editar_gestion(request):
    return render(request, 'editar_gestion.html')

