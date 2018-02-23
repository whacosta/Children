from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class Programa(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=False, null=True)
    edad_ini = models.IntegerField(blank=True, null=True)
    edad_fin = models.IntegerField(blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True)
    objetivo = models.CharField(max_length=40, blank=True, null=True)
    # mock up
    imagen = models.URLField(max_length=200, blank=True, null=True)
    # imagen = models.ImageField(upload_to='programas/iconos', blank=True)

    def __str__(self):
        return("{}".format(self.nombre))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Programa, self).save(*args, **kwargs)


class Ubicacionimplementacion(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    programa = models.ForeignKey(Programa, blank=True, null=False)
    latitud = models.CharField(max_length=30, blank=True, null=True)
    longitud = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=30, blank=True, null=True)
    def __str__(self):
        return("{} - {}".format(self.id, self.ciudad))


class ElementoClave(models.Model):
    COLOR_CHOICES = (
    (1, "Verde"),
    (2, "Amarillo"),
    (3, "Rojo"),
    (4, "Morado"),
    (5, "Azul"),
    )
    ORDEN_CHOICES = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
    )
    # id = models.IntegerField(blank=True, null=True)
    programa = models.ForeignKey(Programa, blank=True, null=False, related_name='elementos_clave')
    nombre = models.CharField(max_length=30, blank=True, null=True)

    orden = models.PositiveSmallIntegerField(choices=ORDEN_CHOICES, null=True, blank=True, default=1)
    slug = models.SlugField(max_length=200, blank=False, null=True)
    color = models.PositiveSmallIntegerField(choices=COLOR_CHOICES, null=True, blank=True, default=1)

    def save(self,*args, **kwargs):

        self.slug = slugify(self.nombre)
        super(ElementoClave, self).save(*args, **kwargs)

    def __str__(self):
        return("{} - {}".format(self.id, self.nombre))


class Tienda(models.Model):
    # Se  supone que este es su pk?
    personalidad = models.CharField(max_length=10, blank=True, null=True)
    elemento_clave = models.ForeignKey(ElementoClave, blank=True, null=True, related_name="personalidades")
    costo = models.IntegerField(blank=True, null=True)
    archivo = models.FileField(upload_to='personalidades/', blank=True, null=True)

class Recurso(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=25, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    content_type = models.ForeignKey(ContentType,blank=True, null=True)
    content_id = models.PositiveIntegerField(blank=True, null=True)
    content = GenericForeignKey('content_type', 'content_id')
    slug = models.SlugField(max_length=200, blank=False, null=True)
    ruta = models.FileField(upload_to='resources/', blank=True, null=True)
    def __str__(self):
        return("{} - {}".format(self.id, self.nombre))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Recurso, self).save(*args, **kwargs)


class ResultadoDeAprendizaje(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    elemento_clave = models.ForeignKey(ElementoClave, blank=True, null=True, related_name="resultados_aprendizaje")
    nivel = models.IntegerField(blank=True, null=True)
    resultado = models.CharField(max_length=255, blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)


class Viaje(models.Model):
    destino = models.CharField(max_length=20, blank=True, null=True)
    elemento_clave = models.ForeignKey(ElementoClave, blank=True, null=True)


class Casa(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    mundo = models.ForeignKey(ElementoClave, blank=True, null=True, related_name="casas")
    slug = models.SlugField(max_length=200, blank=False, null=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)

    def save(self,*args, **kwargs):

        self.slug = slugify(self.nombre)
        super(Casa, self).save(*args, **kwargs)
