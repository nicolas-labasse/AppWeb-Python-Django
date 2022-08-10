
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='eventos/')
    link_compra = models.URLField(max_length=200, blank=True)
    detalle = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-fecha']



class ImagenesEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    images = models.FileField(upload_to='eventos/')

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'


class FondoPagina(models.Model):
    nombre = models.CharField(max_length=100)
    aprobado = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='imagenes/')

    class Meta:
        verbose_name = 'Fondo'
        verbose_name_plural = 'Fondos'