from django.db import models


class Mejoracgm(models.Model):
    servicio = models.CharField(max_length=250, verbose_name='Servicio')
    herramienta_de_monitoreo = models.CharField(
        max_length=250, 
        verbose_name='Herramienta de monitoreo', 
        blank=True,  # Permite que esté vacío en el formulario
        null=True     # Permite que sea nulo en la base de datos
    )
    tipo_de_mejora = models.CharField(max_length=250, verbose_name='Tipo de Mejora')
    numero_peticion = models.CharField(max_length=250, verbose_name='Número Petición')
    numero_wo = models.CharField(max_length=250, verbose_name='Número WO')
    servidor = models.CharField(max_length=500, verbose_name='Servidor')
    variable = models.TextField(verbose_name='Variable de la alerta')
    peticion_reincidente = models.CharField(max_length=250, verbose_name='Petición Reincidente')
    peticion_anterior = models.CharField(max_length=250, verbose_name='N° Petición Anterior')
    observaciones = models.TextField(verbose_name='Observaciones')
    fecha_hora_mejora = models.DateTimeField("Fecha y Hora Mejora", auto_now_add=False)
    area_responsable = models.CharField(max_length=250, verbose_name='Área Responsable')
    mejora_creada_por = models.CharField(max_length=250, verbose_name='Mejora Creada Por')
    estado = models.CharField(max_length=250, verbose_name='Estado')
    solucion = models.TextField(verbose_name='Descripción')
    fecha_hora = models.DateTimeField(null=True, blank=True, verbose_name='fecha y hora de cierre de la mejora')

    def __str__(self):
       return (
           f"{self.servicio} - {self.herramienta_de_monitoreo} - {self.tipo_de_mejora} - "
           f"{self.numero_peticion} - {self.numero_wo} - {self.servidor} - "
           f"{self.variable} - {self.peticion_reincidente} - {self.peticion_anterior} - "
           f"{self.observaciones} - {self.fecha_hora_mejora} - {self.area_responsable} - {self.mejora_creada_por}"
           f"{self.estado} - {self.solucion} - {self.fecha_hora}"
       )

    class Meta:
        verbose_name_plural = 'Mejoras CGM'
        verbose_name = 'Mejora CGM'


