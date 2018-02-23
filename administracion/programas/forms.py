from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from usuarios.models import *
from .models import *
from django.forms import ModelForm

class ElementoClaveForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ElementoClaveForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        

    class Meta:
        model = ElementoClave
        exclude = ['slug','programa']



class ResultadoAprendizajeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ResultadoAprendizajeForm, self).__init__(*args, **kwargs)
        self.fields['nivel'] = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
        self.fields['resultado'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        self.fields['orden'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        

    class Meta:
        model = ResultadoDeAprendizaje
        exclude = ['elemento_clave']

class TiendaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TiendaForm, self).__init__(*args, **kwargs)
        self.fields['personalidad'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Ingrese el nombre de la personalidad"}))
        self.fields['costo'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Ingrese cantidad de monedas"}))
        self.fields['archivo'] = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))


    class Meta:
        model = Tienda
        exclude = ['elemento_clave']

class CasaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CasaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        self.fields['orden'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        

    class Meta:
        model = Casa
        exclude = ['mundo','slug']


class RecursoClaveForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecursoClaveForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        self.fields['descripcion'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        self.fields['ruta'] = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model = Recurso
        exclude = ['content_type', 'content_id','content', 'slug']