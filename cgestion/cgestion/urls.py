"""
URL configuration for cgestion project.

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

from django.contrib import admin
from django.urls import path, include
from gestiones import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.listar_gestiones, name='listar_gestiones'),  # Ruta para la raíz
    path('creargestion/', views.creargestion, name='creargestion'),
    path('creargestion/editar_gestion/<int:id>/',views.editar_gestion, name='editar_gestion'),
    path('editar_gestion/<int:id>/',views.editar_gestion, name='editar_gestion'),
    path('registro_usuario/', views.register_page, name='registro_usuario'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('enviar-email/<int:gestion_id>', views.enviar_gestion_email, name='enviar_email'),
    path('descargar_gestiones/', views.descargar_gestiones, name='descargar_gestiones'),
    path('listar_gestiones_en_investigacion/', views.listar_gestiones_en_investigacion, name='listar_gestiones_en_investigacion'),
    path('grafico/', views.grafico_gestiones, name='grafico_gestiones'),
    path('grafico_gestiones_eventos/', views.grafico_gestiones_eventos, name='grafico_gestiones_eventos'),
    path('grafico_gestiones_no_gioti/', views.grafico_gestiones_no_gioti, name='grafico_gestiones_no_gioti'),
    
    
    path("cambiar-contrasena/", views.change_password, name="cambiar_contrasena"),
    path("perfil/", views.perfil, name="perfil"),

    ######## urls de mejorascgm#####

    path('mejorascgm/', include('mejorascgm.urls')),
]
