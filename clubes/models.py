from django.db import models
from programas.models import Programa, ElementoClave
from django.utils.text import slugify
import datetime

# Create your models here.
class Club(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    programa = models.ForeignKey(Programa, blank=True, null=False, related_name='clubes', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=25, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=False, null=True)
    ahorros = models.IntegerField(blank=True, null=True)
    nivel = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    def __str__(self):
        return("{}".format(self.nombre))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        self.ahorros = 0
        self.nivel = 0
        self.color="#FFFFFF"
        self.fecha = datetime.date.today()
        super(Club, self).save(*args, **kwargs)

class Cofre(models.Model):
    club = models.ForeignKey( Club,blank=True, null=True, on_delete=models.CASCADE)
    premio = models.IntegerField(blank=True, null=True)

class Horariochat(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    club = models.ForeignKey( Club,blank=True, null=True, on_delete=models.CASCADE)
    dia = models.CharField(max_length=9, blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    estado = models.BooleanField(default=True,blank=True)

class ElementoClub(models.Model):
    mundo = models.ForeignKey( ElementoClave ,blank=True, null=True, on_delete=models.CASCADE)
    club = models.ForeignKey( Club,blank=True, null=True, on_delete=models.CASCADE)
    color = models.CharField(max_length=10, blank=True, null=True)

class Cita(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    dia = models.DateField(blank=True, null=True)
    evento = models.CharField(max_length=225, blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)

    def __str__(self):
        return(self.evento+" - "+self.dia.strftime("%Y-%m-%d"))

    def get_clubes(self):
        clubes_cita = ClubCita.objects.filter(cita=self)
        clubes = []
        for c in clubes_cita:
            clubes.append(c.club)
        return clubes

class ClubCita(models.Model):
    club = models.ForeignKey(Club,blank=False,null=False, on_delete=models.CASCADE)
    cita = models.ForeignKey(Cita,blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return (str(self.club) +" - "+str(self.cita))
