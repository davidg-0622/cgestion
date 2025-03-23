from django.contrib import admin
import openpyxl
import csv
from django.http import HttpResponse
from .models import Gestion
from mejorascgm.models import Mejoracgm

# ==========================
# Administración de Gestion
# ==========================
class PageAdmin(admin.ModelAdmin):
    readonly_fields = ('responsable_gioti',)  
    search_fields = ('servicio', 'tipo_de_gestion', 'numero_caso', 'detectada_por', 
                     'causado_por_certificado_digital', 'incidente_generado_por_OC', 
                     'atribuible_a', 'tipo_de_falla', 'detalle', 'tipo_causa', 'causa', 
                     'validaciones', 'solucion', 'responsable_gioti', 'fecha_hora_inicial', 
                     'fecha_hora_final', 'postular_amg', 'gioti')
    list_filter = ('servicio', 'tipo_de_gestion')
    list_display = ('numero_caso', 'servicio', 'tipo_de_gestion', 'detectada_por', 
                    'causado_por_certificado_digital', 'incidente_generado_por_OC', 
                    'atribuible_a', 'tipo_de_falla', 'detalle', 'tipo_causa', 'causa', 
                    'validaciones', 'solucion', 'responsable_gioti', 'fecha_hora_inicial', 
                    'fecha_hora_final', 'postular_amg', 'gioti')    

    # Método para exportar a Excel
    actions = ["exportar_excel"]

    def exportar_excel(self, request, queryset):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["ID", "Servicio", "Tipo de Gestión", "Número de Caso", "Detectada Por",
                   "Causado por Certificado Digital", "Incidente Generado por OC", 
                   "Atribuible A", "Tipo de Falla", "Detalle", "Tipo de Causa", "Causa", 
                   "Validaciones", "Solución", "Responsable GIOTI", "Fecha Hora Inicial", 
                   "Fecha Hora Final", "Postular AMG", "GIOTI"])  # Encabezados

        for obj in queryset:
            ws.append([obj.id, obj.servicio, obj.tipo_de_gestion, obj.numero_caso, 
                       obj.detectada_por, obj.causado_por_certificado_digital, 
                       obj.incidente_generado_por_OC, obj.atribuible_a, obj.tipo_de_falla, 
                       obj.detalle, obj.tipo_causa, obj.causa, obj.validaciones, 
                       obj.solucion, obj.responsable_gioti, obj.fecha_hora_inicial, 
                       obj.fecha_hora_final, obj.postular_amg, obj.gioti])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="gestion.xlsx"'
        wb.save(response)

        return response

    exportar_excel.short_description = "Exportar a Excel"

admin.site.register(Gestion, PageAdmin)

# ==========================
# Administración de Mejoracgm
# ==========================
class MejorasAdmin(admin.ModelAdmin):
    readonly_fields = ('mejora_creada_por',)
    
    list_display = ('servicio', 'herramienta_de_monitoreo', 'tipo_de_mejora', 'numero_peticion', 'numero_wo', 'servidor',
                    'variable', 'peticion_reincidente', 'peticion_anterior', 'observaciones',
                    'fecha_hora_mejora', 'area_responsable', 'mejora_creada_por', 'estado', 'solucion', 'fecha_hora')

    search_fields = ('servicio', 'herramienta_de_monitoreo', 'tipo_de_mejora', 'numero_peticion', 'numero_wo', 'servidor',
                     'variable', 'peticion_reincidente', 'peticion_anterior', 'observaciones',
                     'fecha_hora_mejora', 'area_responsable', 'mejora_creada_por', 'estado', 'solucion', 'fecha_hora')

    list_filter = ('servicio', 'herramienta_de_monitoreo', 'tipo_de_mejora', 'numero_peticion', 'numero_wo',
                   'fecha_hora_mejora', 'fecha_hora')

    actions = ["exportar_csv"]

    def exportar_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="mejoras.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Servicio", "Herramienta de Monitoreo", "Tipo de Mejora", "Número de Petición",
                         "Número WO", "Servidor", "Variable", "Petición Reincidente", "Petición Anterior",
                         "Observaciones", "Fecha y Hora de Mejora", "Área Responsable", "Mejora Creada Por",
                         "Estado", "Solución", "Fecha y Hora"])  

        for obj in queryset:
            writer.writerow([
                obj.id,
                obj.servicio,
                obj.herramienta_de_monitoreo,
                obj.tipo_de_mejora,
                obj.numero_peticion,
                obj.numero_wo,
                obj.servidor,
                obj.variable,
                obj.peticion_reincidente,
                obj.peticion_anterior,
                obj.observaciones,
                obj.fecha_hora_mejora,
                obj.area_responsable,
                obj.mejora_creada_por,
                obj.estado,
                obj.solucion,
                obj.fecha_hora
            ])

        return response

    exportar_csv.short_description = "Exportar Mejoras a CSV"

admin.site.register(Mejoracgm, MejorasAdmin)

# ==========================
# Configuración general del panel de administración
# ==========================
admin.site.site_header = "CGESTION"
admin.site.site_title = "CGESTION"
admin.site.index_title = "Monitoreo"
