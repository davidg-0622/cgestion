from django.db import models

# Create your models here.
class Gestion(models.Model):
    servicio = models.CharField(max_length=250)
    tipo_de_gestion = models.CharField(max_length=250)
    numero_caso = models.CharField(max_length=250)
    detectada_por = models.CharField(max_length=250)
    causado_por_certificado_digital = models.BooleanField(default=False)
    incidente_generado_por_OC = models.BooleanField(default=False)
    atribuible_a = models.CharField(max_length=30)
    tipo_de_falla = models.CharField(max_length=30)
    detalle = models.TextField()
    tipo_causa = models.CharField(max_length=30)
    causa = models.TextField()
    validaciones = models.TextField()
    solucion = models.TextField()
    responsable_gioti = models.CharField(max_length=250)
    fecha_hora_inicial = models.DateTimeField("Fecha y Hora Inicial", auto_now=False, auto_now_add=False)
    fecha_hora_final = models.DateTimeField("Fecha y Hora Final", auto_now=False, auto_now_add=False)
    postular_amg = models.BooleanField(default=False)
    gioti = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.servicio} - {self.tipo_de_gestion} - {self.numero_caso} - {self.detectada_por} - "
            f"{self.causado_por_certificado_digital} - {self.incidente_generado_por_OC} - "
            f"{self.atribuible_a} - {self.tipo_de_falla} - {self.detalle} - "
            f"{self.tipo_causa} - {self.causa} - {self.validaciones} - {self.solucion} - "
            f"{self.responsable_gioti} - {self.fecha_hora_inicial} - {self.fecha_hora_final} - "
            f"{self.postular_amg} - {self.gioti}"
        )
        
        
class Servicio(models.Model):
    servicio = models.CharField(max_length=300)
    fecha_creacion = models.DateTimeField("Fecha creacion", auto_now=True)
    
    def __str__(self):
        return f"{self.servicio} - {self.fecha_creacion}"
