from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from usuarios.models import Nino
from .models import *
from usuarios.models import UsuarioClub
from django.forms import ModelForm

class ClubForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClubForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        self.fields['programa'] = forms.ModelChoiceField(queryset=Programa.objects.filter(tipo=2))


    class Meta:
        model = Club
        exclude = ['slug']


class CitaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):   
        super(CitaForm, self).__init__(*args, **kwargs)
        self.fields['dia'] = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control datepicker', 'data-provide':"datepicker"}))
        self.fields['evento'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        self.fields['hora_inicio'] = forms.TimeField(input_formats=['%I:%M %p'],widget=forms.TimeInput(attrs={'class':'form-control','format':'%I:%M %p'}))
        self.fields['hora_fin'] = forms.TimeField(input_formats=['%I:%M %p'],widget=forms.TimeInput(attrs={'class':'form-control','format':'%I:%M %p'}))

    class Meta:
        model = Cita
        exclude = ()

    def save(self,clubes=None,commit=True,*args, **kwargs):
        cita = super(CitaForm, self).save(commit=False, *args, **kwargs)
        if commit:
            cita.save()
            for club in clubes:
                c = ClubCita(cita=cita,club=club)
                c.save()
        return cita

class CitaClubForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CitaClubForm, self).__init__(*args, **kwargs)
        self.fields['dia'] = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control datepicker', 'data-provide':"datepicker"}))
        self.fields['evento'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        self.fields['hora_inicio'] = forms.TimeField(input_formats=['%I:%M %p'],widget=forms.TimeInput(attrs={'class':'form-control','format':'%I:%M %p'}))
        self.fields['hora_fin'] = forms.TimeField(input_formats=['%I:%M %p'],widget=forms.TimeInput(attrs={'class':'form-control','format':'%I:%M %p'}))

    class Meta:
        model = Cita
        exclude = ()

    def save(self,club=None,commit=True,*args, **kwargs):
        cita = super(CitaClubForm, self).save(commit=False, *args, **kwargs)
        if commit:
            cita.save()
            c = ClubCita(cita=cita,club=club)
            c.save()
        return cita
