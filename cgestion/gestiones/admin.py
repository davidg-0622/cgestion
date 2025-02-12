from django.contrib import admin
from .models import Gestion
from mejorascgm.models import Mejoracgm


from django.contrib import admin



class PageAdmin(admin.ModelAdmin):
    readonly_fields = ('responsable_gioti',)  # Nota la coma al final de la tupla
    
    # activar el buscador en los 18 campos 
    search_fields =('servicio', 'tipo_de_gestion', 'numero_caso', 'detectada_por', 'causado_por_certificado_digital','incidente_generado_por_OC', 'atribuible_a', 'tipo_de_falla', 'detalle', 'tipo_causa', 'causa', 'validaciones', 'solucion', 'responsable_gioti', 'fecha_hora_inicial', 'fecha_hora_final', 'postular_amg', 'gioti' )
  
  
  # Filtros de lista (opcional, puedes agregar más)
    list_filter = ('servicio', 'tipo_de_gestion')
    

  # sacar columnas que necesito 
    list_display = ('numero_caso','servicio', 'tipo_de_gestion', 'detectada_por', 'causado_por_certificado_digital','incidente_generado_por_OC', 'atribuible_a', 'tipo_de_falla', 'detalle', 'tipo_causa', 'causa', 'validaciones', 'solucion', 'responsable_gioti', 'fecha_hora_inicial', 'fecha_hora_final', 'postular_amg', 'gioti')    
    
    # sacar columnas que necesito 
    
   
# Registrar el modelo en el admin
admin.site.register(Gestion, PageAdmin)

    


# Configurar el título del panel de administración
title = 'CGESTION'
admin.site.site_header = title  # Título en la cabecera del admin
admin.site.site_title = title   # Título en la pestaña del navegador

admin.site.index_title = "Monitoreo"  # Título de la página de índice 


class MejorasAdmin(admin.ModelAdmin):
    readonly_fields = ('mejora_creada_por',)
    list_display = ('servicio', 'herramienta_de_monitoreo', 'tipo_de_mejora', 'numero_peticion', 'numero_wo', 'servidor','variable', 'peticion_reincidente', 'peticion_anterior', 'observaciones','fecha_hora_mejora', 'area_responsable', 'mejora_creada_por', 'estado', 'solucion', 'fecha_hora'  )  # Reemplaza con los campos que quieras mostrar
    search_fields = ('servicio', 'herramienta_de_monitoreo', 'tipo_de_mejora', 'numero_peticion', 'numero_wo', 'servidor','variable', 'peticion_reincidente', 'peticion_anterior', 'observaciones','fecha_hora_mejora', 'area_responsable', 'mejora_creada_por', 'estado', 'solucion', 'fecha_hora')  # Campos por los que se puede buscar
    list_filter = ('servicio', 'herramienta_de_monitoreo', 'tipo_de_mejora','numero_peticion', 'numero_wo','fecha_hora_mejora', 'fecha_hora')  # Filtros opcionales

admin.site.register(Mejoracgm, MejorasAdmin)
