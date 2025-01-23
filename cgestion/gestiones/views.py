from django.shortcuts import render


def inicio(request):
    return render(request, 'gestiones.html')


def editar_gestion(request):
    return render(request, 'editar_gestion.html')

def creargestion(request):
    return render(request, 'crear_gestion.html')  # El nombre de la plantilla debe ir entre comillas
