"""
URL configuration for mejorascgm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('crear_mejora/', views.crear_mejora, name='crear_mejora'),
    path('listar_mejora/', views.listar_mejora, name='listar_mejora'),
    path('listar_mejoras_cerradas/', views.listar_mejoras_cerradas, name='listar_mejoras_cerradas'),
    path('editar_mejora/<int:id>/', views.editar_mejora, name='editar_mejora'),
    path('enviar_mejora_email/<int:mejora_id>/', views.enviar_mejora_email, name='enviar_mejora_email'),
]
