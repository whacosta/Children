# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import *
from django.forms import ModelForm


class FormLogin(AuthenticationForm):
    username = forms.CharField( 
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Ingrese su usuario'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Ingrese su contrasenia'}
        )
    )

class UsuarioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Ingrese el nombre",'class':'form-control'}))
        self.fields['apellido'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Ingrese el apellido",'class':'form-control'}))
        self.fields['usuario'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Ingrese el nombre de usuario",'class':'form-control'}))
        self.fields['mail'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Ingrese el mail",'class':'form-control'}))
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Ingrese la contrasena",'class':'form-control'}))
        print(self.instance)
        if self.instance.pk!=None:

            self.fields['pic_profile'] = forms.ImageField(required=False,widget=forms.FileInput(
                                                        attrs={'class':'dropify',
                                                        'data-default-file':self.instance.pic_profile.url,
                                                        'multiple accept': 'image/*',
                                                        ' data-allowed-file-extensions':'jpg png'}))
            del self.fields['password']
        else:
            self.fields['pic_profile'] = forms.ImageField(required=False,widget=forms.FileInput(
                                                        attrs={'class':'dropify',
                                                        'data-default-file':'/media/ImagesProfile/people.png',
                                                        'multiple accept': 'image/*',
                                                        ' data-allowed-file-extensions':'jpg png'}))

    class Meta:
        model = Usuario
        exclude = ['is_active','is_admin','role','cambio_password','fecha_registro','last_login',]

    def save(self,role=None, commit=True,*args, **kwargs):
        usuario = super(UsuarioForm, self).save(commit=False, *args, **kwargs)
        if role == None:
            usuario.role = 1
        else:
            usuario.role = role
        if commit:
            usuario.save()
        return usuario

    # def clean_cedula(self):
    #     cedula = self.cleaned_data['cedula']
    #     qs = Paciente.objects.filter(cedula=cedula)

    #     try:
    #         qs = qs.exclude(pk=self.id)
    #     except Exception, e:
    #         pass
            
    #     if qs.count() > 0:
    #         raise ValidationError('Cédula ya existe')
    #     return cedula

class NinoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NinoForm, self).__init__(*args, **kwargs)
        self.fields['cod_apadr'] = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':"Ingrese el código",'class':'form-control', 'maxlength':12}))
        self.fields['cedula'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Ingrese la cedula",'class':'form-control','maxlength':10}))
        self.fields['fecha_nacimiento'] = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control datepicker', 'data-provide':"datepicker"}))

    class Meta:
        model = Nino
        exclude = ['slug']
        
        
