from django.db import models

# Create your models here.

class Servicio(models.Model):
    servicio = models.TextField()


class RegistroVenta(models.Model):
    CLASIFICACION = (
        (i.servicio, i.servicio) for i in Servicio.objects.all()
    ) 
   
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    empresa = models.TextField()
    ruc = models.TextField()
    precio = models.FloatField()
    tipo = models.TextField(choices=(CLASIFICACION))

class RedNeuronalResultados(models.Model):
    CLASIFICACION = (
        (i.servicio, i.servicio) for i in Servicio.objects.all().order_by('-id')
    ) 

    PERIODO = (
        ('DIAS', 'DIAS'),
        ('SEMANAS', 'SEMANAS'),
        ('MESES', 'MESES'),
    )

    clasificacion = models.TextField(choices=(CLASIFICACION))
    periodo = models.TextField(choices=(PERIODO))
    look_back = models.IntegerField()
    neuronas = models.IntegerField()
    epocas = models.IntegerField()

"""
class DatosRedNeuronal(models.Model):
    TIPO = (
        ('TRAIN', 'TRAIN'),
        ('TEST', 'TEST'),
    )

    fecha = models.DateField(auto_now=False, auto_now_add=False)
    precio = models.FloatField(blank=True, null=True)
    dam = models.FloatField(blank=True, null=True)
    pema = models.FloatField(blank=True, null=True)
    rmse = models.FloatField(blank=True, null=True)
    precio_real = models.FloatField(blank=True, null=True)
    tipo = models.TextField(choices=(TIPO), blank=True, null=True)
    entrenamiento = models.ForeignKey("prediccion.RedNeuronalResultados", related_name='getResultadosServicios', on_delete=models.CASCADE)
"""

class DatosRedNeuronalTest(models.Model):

    #dam = models.FloatField(blank=True, null=True)
    #pema = models.FloatField(blank=True, null=True)
    #rmse = models.FloatField(blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)
    future = models.DateField(auto_now=False, auto_now_add=False)
    entrenamiento = models.ForeignKey("prediccion.RedNeuronalResultados", related_name='getResultadosServiciosTest', on_delete=models.CASCADE)
    #venta = models.ForeignKey("prediccion.RegistroVenta", related_name='getResultadosVentaTest', on_delete=models.CASCADE)
    #real = models.FloatField(blank=True, null=True)
    #fecha = models.DateField(auto_now=False, auto_now_add=False)


class DatosRedNeuronalTrain(models.Model):

    dam = models.IntegerField(blank=True, null=True)
    pema = models.IntegerField(blank=True, null=True)
    rmse = models.IntegerField(blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)
    #future = models.DateField(auto_now=False, auto_now_add=False)
    entrenamiento = models.ForeignKey("prediccion.RedNeuronalResultados", related_name='getResultadosServiciosTrain', on_delete=models.CASCADE)
    #venta = models.ForeignKey("prediccion.RegistroVenta", related_name='getResultadosVentaTrain', on_delete=models.CASCADE)
    real = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(auto_now=False, auto_now_add=False)

    



