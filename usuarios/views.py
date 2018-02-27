# -*- coding: utf-8 -*-
#Importamos la vista genérica FormView
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import FormLogin
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import TemplateView,View
from usuarios.models import *
from usuarios.forms import UsuarioForm,NinoForm
from django.http import HttpResponse
from django.forms import ModelForm
from django import forms
from datetime import date
import json

class Login(FormView):
    #Establecemos la plantilla a utilizar
    template_name = 'login.html'
    #Le indicamos que el formulario a utilizar es el formulario de autenticación de Django
    form_class = FormLogin
    #Le decimos que cuando se haya completado exitosamente la operación nos redireccione a la url bienvenida de la aplicación administrator
    success_url =reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        #Si el usuario está autenticado entonces nos direcciona a la url establecida en success_url
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        #Sino lo está entonces nos muestra la plantilla del login simplemente
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)
 
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

class AdministratorView(TemplateView):
    template_name = 'administradores.html'
    def get_context_data(self, **kwargs):
        context = super(AdministratorView, self).get_context_data(**kwargs)
        usuarios = Usuario.objects.filter(role=1)
        context['usuarios'] = usuarios
        context['formulario'] = UsuarioForm(instance=None)
        return context

class FacilitatorView(TemplateView):
    template_name = 'facilitadores.html'
    def get_context_data(self, **kwargs):
        context = super(FacilitatorView, self).get_context_data(**kwargs)
        usuarios = Usuario.objects.filter(role=2) | Usuario.objects.filter(role=3)
        context['usuarios'] = usuarios
        context['formulario'] = UsuarioForm(instance=None)
        return context

def save_administrator(request):
    if request.POST:
        if request.POST.get('id_admin'):
            admin = Usuario.objects.get(pk=request.POST.get('id_admin'))
            form = UsuarioForm(request.POST, request.FILES, instance=admin)
        else:
            form = UsuarioForm(request.POST, request.FILES)
        print( request.FILES)
        print(form)
        if form.is_valid():
            print(form.cleaned_data['pic_profile'])
            if 'pic_profile'  in request.FILES:
                filename = request.FILES['pic_profile']
                print(filename)
            usuario = form.save()
            # No se guarda la imagen todavia
            # usuario.pic_profile = form.cleaned_data['pic_profile']
            # usuario.save()
            return HttpResponse(1)
        else:
            print(form.errors)
            return HttpResponse(0)

def save_facilitator(request):
    if request.POST:
        role = request.POST.get('tipo')
        print (role)
        if request.POST.get('id_facilitator'):
            admin = Usuario.objects.get(pk=request.POST.get('id_facilitator'))
            form = UsuarioForm(request.POST, request.FILES, instance=admin)
        else:
            form = UsuarioForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data['pic_profile'])
            if 'pic_profile'  in request.FILES:
                filename = request.FILES['pic_profile']
                print(filename)
            usuario = form.save(role=role)
            # No se guarda la imagen todavia
            # usuario.pic_profile = form.cleaned_data['pic_profile']
            # usuario.save()
            return HttpResponse(1)
        else:
            print(form.errors)
            return HttpResponse(0)

def delete_administrator(request):
    if request.POST:
        id_admin = request.POST.get('id_admin')
        try:
            admin = Usuario.objects.get(pk=id_admin)
            admin.delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)
def edit_administrator(request):
    if request.method == 'POST':
        id_admin = request.POST.get('id_admin')
        admin = Usuario.objects.get(pk=id_admin)
        form = UsuarioForm(instance=admin)
        return render(request, 'editar_usuario.html', {
            'formulario': form,
            'id_admin':id_admin
            })
    else:
        mensaje = "cero"
        return HttpResponse(mensaje, content_type='application/json')

def save_edit_administrator(request):
    if request.method == 'POST':
        admin = Usuario.objects.get(pk=request.POST.get('id_admin'))
        form = UsuarioForm(request.POST, request.FILES, instance=admin)
        print(form.is_valid())
        if form.is_valid():
            admin = form.save(role=admin.role)
            print(admin)
            return HttpResponse(json.dumps({'usuario':admin.usuario,'nombre':admin.nombre,
                'apellido':admin.apellido,'mail':admin.mail}), content_type='application/json')
        else:
            return HttpResponse(0)

class NinosView(View):
    template_name = 'ninos.html'
    def get(self, request):
        context = {
            'ninos':  Nino.objects.all(),
            'formulario': NinoForm(instance=None)
        }
        return render(request,self.template_name, context)

def save_nino(request):
    if request.POST:
        nino = NinoForm(request.POST)
        if nino.is_valid():
            nino.save()
            return HttpResponse(1)
        else:
            return HttpResponse(0)


def delete_nino(request):
    if request.POST:
        id_nino = request.POST.get('id_nino')
        try:
            nino = Nino.objects.get(pk=id_nino)
            nino.delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

def edit_nino(request):
    if request.method == 'POST':
        id_nino = request.POST.get('id_nino')
        nino= Nino.objects.get(pk=id_nino)
        form = NinoForm(instance=nino)
        return render(request, 'editar_nino.html', {
            'formulario': form,
            'id_nino':id_nino
            })
    else:
        mensaje = "cero"
        return HttpResponse(mensaje, content_type='application/json')

def save_edit_nino(request):
    if request.method == 'POST':
        nino = Nino.objects.get(pk=request.POST.get('id_nino'))
        form = NinoForm(request.POST, instance=nino)
        if form.is_valid():
            form.save()
            return HttpResponse(1)
        else:
            return HttpResponse(0)
