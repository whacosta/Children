from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from clubes.models import Club
from programas.models import ElementoClave, Tienda, Casa
from django.contrib.auth.models import UserManager,BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from datetime import datetime
from django.core.validators import validate_email

class UserManager(BaseUserManager):
    def create_user(self, usuario, password=None, **kwargs):
        print("create user")
        user = self.model(usuario=usuario, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, usuario, password, **kwargs):
        print("create superuser")
        user = self.model(usuario=usuario, **kwargs)
        user.set_password(password)
        user.save()
        return user

class Usuario(AbstractBaseUser):
    ADMINISTRADOR_MASTER= 1
    FACILITADOR = 2
    CO_FACILITADOR = 3
    ROLE_CHOICES = (
        (ADMINISTRADOR_MASTER, 'Administrador_master'),
        (FACILITADOR, 'Facilitador'),
        (CO_FACILITADOR, 'Co_Facilitador'),
    )
    usuario = models.CharField(max_length=15,unique=True)
    nombre = models.CharField(max_length=30,blank=True,null=True)
    apellido = models.CharField(max_length=30,blank=True,null=True)
    mail = models.CharField(max_length=30,null=False,blank=True,unique=True)
    pic_profile = models.ImageField(upload_to='ImagesProfile', null=True, blank=True,verbose_name="Imagen de perfil", default = 'ImagesProfile/people.png')
    fecha_registro = models.DateTimeField(default=datetime.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True, default=ADMINISTRADOR_MASTER)
    cambio_password = models.CharField(max_length=150,blank=True,null=True)
    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['is_admin','mail','is_active']
    objects = UserManager()
    def get_full_name(self):
        return self.nombre
    def get_short_name(self):
        return self.usuario
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin
    def __unicode__(self):
        return self.usuario
    def clean(self):
        super(Usuario, self).clean()
        mail  = validate_email(self.mail)
        if "sha256" not in self.password and len(self.password)<70:
            self.set_password(self.password)
        #existMail = validate_email(self.mail, verify=True)
        print(self.password)
        if mail == False and self.mail!="":
            raise ValidationError('Correo no válido')



class UsuarioClub(models.Model):
    club = models.ForeignKey(Club,blank=True, null=False, on_delete=models.CASCADE)
    usuario = models.ForeignKey( Usuario,blank=True, null=False, on_delete=models.CASCADE)
    estado = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return(str(self.club)+" - "+str(self.usuario))

class Nino(models.Model):
    ESTADOS = (
        ('AA', 'Apadrinado y Activo'),
        ('AI', 'Apadrinado e Inactivo'),
        ('NA', 'Nunca ha sido apadrinado'),
    )
    cod_apadr = models.IntegerField(blank=True, null=False)
    cedula = models.CharField(max_length=10, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=False, null=True)
    latitud = models.CharField(max_length=25, blank=True, null=True, default='0')
    longitud = models.CharField(max_length=25, blank=True, null=True, default='0')
    estado = models.CharField(max_length=2, choices=ESTADOS, blank=True, null=True)

    def __str__(self):
        return("{}".format(self.cod_apadr))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.cod_apadr)
        self.latitud = 0
        self.longitud = 0
        super(Nino, self).save(*args, **kwargs)
    def clean_latitud(self):
        return 10
    def clean_latitud(self):
        return 10
    def age(self):
        import datetime
        dob = self.fecha_nacimiento
        tod = datetime.date.today()
        my_age = (tod.year - dob.year) - int((tod.month, tod.day) < (dob.month, dob.day))
        return my_age
class NinoClub(models.Model):
    nino = models.ForeignKey(Nino,blank=True, null=False, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, blank=True, null=False, on_delete=models.CASCADE)
    fecha = models.DateField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    ahorro = models.IntegerField(blank=True, null=True)

class ElementoNino(models.Model):
    mundo = models.ForeignKey(ElementoClave,blank=True, null=True, on_delete=models.CASCADE) #Elemento clave
    nino = models.ForeignKey(Nino,blank=True, null=False, on_delete=models.CASCADE)

class Compra(models.Model):
    nino = models.IntegerField(blank=True, null=False)
    personalidad = models.ForeignKey(Tienda, blank=True, null=False, on_delete=models.CASCADE)

class Avatar(models.Model):
    nino = models.ForeignKey(Nino,blank=True, null=False, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, blank=True, null=False, on_delete=models.CASCADE)
    alias = models.CharField(max_length=10, blank=True, null=True)

class CasaNino(models.Model):
    casa = models.ForeignKey(Casa,blank=True, null=False, on_delete=models.CASCADE)
    nino = models.ForeignKey(Nino, blank=True, null=False, on_delete=models.CASCADE)

class Actividad(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    casa = models.ForeignKey(Casa,blank=True, null=False, related_name='actividades', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=False, null=True)
    nivel = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=10, blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)
    premio = models.IntegerField(blank=True, null=True)
    tiempo_esperado = models.TimeField(blank=True, null=True)
    def __str__(self):
        return("{}".format(self.nombre))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Actividad,self).save(*args,**kwargs)



class ActividadNino(models.Model):
    # id = models.IntegerField(blank=True, null=True)
    actividad = models.ForeignKey(Actividad,blank=True, null=False, on_delete=models.CASCADE)
    nino = models.ForeignKey(Nino, blank=True, null=False, on_delete=models.CASCADE)
    fecha = models.DateField(blank=True, null=True)
    puntaje = models.IntegerField(blank=True, null=True)
    disponible = models.BooleanField(default=True,blank=True)
