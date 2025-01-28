from django.db import models

# Create your models here.
class Gestion(models.Model):
    servicio = models.CharField(max_length=250, verbose_name='Servicio')
    tipo_de_gestion = models.CharField(max_length=250, verbose_name='Tipo de gestion')
    numero_caso = models.CharField(max_length=250, verbose_name='Numero de caso')
    detectada_por = models.CharField(max_length=250, verbose_name='Detectado por')
    causado_por_certificado_digital = models.BooleanField(default=False, verbose_name='Causado por certificado digital')
    incidente_generado_por_OC = models.BooleanField(default=False, verbose_name='Incidente generado por OC')
    atribuible_a = models.CharField(max_length=30, verbose_name='Atribuible a')
    tipo_de_falla = models.CharField(max_length=30, verbose_name='Tipo de falla')
    detalle = models.TextField(verbose_name='Detalle')
    tipo_causa = models.CharField(max_length=30, verbose_name='Tipo_causa')
    causa = models.TextField(verbose_name='Causa')
    validaciones = models.TextField(verbose_name='Validaciones')
    solucion = models.TextField(verbose_name='Solucion')
    responsable_gioti = models.CharField(max_length=250, verbose_name='Responsable gioti')
    fecha_hora_inicial = models.DateTimeField("Fecha y Hora Inicial", auto_now=False, auto_now_add=False )
    fecha_hora_final = models.DateTimeField("Fecha y Hora Final", auto_now=False, auto_now_add=False)
    postular_amg = models.BooleanField(default=False, verbose_name='Postular AMG')
    gioti = models.BooleanField(default=False, verbose_name='GIOTI')

    def __str__(self):
        return (
            f"{self.servicio} - {self.tipo_de_gestion} - {self.numero_caso} - {self.detectada_por} - "
            f"{self.causado_por_certificado_digital} - {self.incidente_generado_por_OC} - "
            f"{self.atribuible_a} - {self.tipo_de_falla} - {self.detalle} - "
            f"{self.tipo_causa} - {self.causa} - {self.validaciones} - {self.solucion} - "
            f"{self.responsable_gioti} - {self.fecha_hora_inicial} - {self.fecha_hora_final} - "
            f"{self.postular_amg} - {self.gioti}"
        )
    
    
    class Meta:
        verbose_name = 'Gestion'
        verbose_name_plural = 'Gestiones'
        ordering=['-id']
    

        
        
        
class Servicio(models.Model):
    servicio = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField("Fecha creacion", auto_now=True)
    
    def __str__(self):
        return f"{self.servicio} - {self.fecha_creacion}"
