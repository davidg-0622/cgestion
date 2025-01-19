from django.shortcuts import render

def creargestion(request):
    return render(request, 'index.html')  # El nombre de la plantilla debe ir entre comillas


def inicio(request):
    return render(request, 'index.html')


def editar_gestion(request):
    return render(request, 'editar_gestion.html')
