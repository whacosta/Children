from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import TemplateView, View, ListView
from django.http import HttpResponse
from django.forms import ModelForm
from programas.models import Programa
from usuarios.models import NinoClub,Nino,UsuarioClub,Usuario
from django import forms
from .models import *
from .forms import *
import datetime
import json
from django.template import defaultfilters
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
import json

# Create your views here.
class ClubesView(ListView):
    template_name = 'clubes.html'
    def get(self, request):
        club_by_user= []
        count_ninos= []
        lista = UsuarioClub.objects.filter(usuario__usuario=request.user.usuario).only('usuario', 'club')
        for variable in lista:
            club=Club.objects.get(nombre=variable.club)
            nino_count = NinoClub.objects.filter(club__nombre=club.nombre).count()
            count_ninos.append(nino_count)
            club_by_user.append(club)
           
        context = {
            'clubes':  zip(club_by_user,count_ninos),
            'formulario': ClubForm(instance=None)
        }
        return render(request,self.template_name, context)

class ClubView(View):
    template_name = 'club.html'
    def get(self, request, club):
        obj_club = Club.objects.filter(slug=club)
        obj_ninos = NinoClub.objects.filter(club=obj_club)
        obj_facilitadores = UsuarioClub.objects.filter(club=obj_club)
        form = CitaClubForm()
        lista_citas = []

        club_citas_pendientes = ClubCita.objects.filter(club=obj_club,
                                            cita__dia__gte=( datetime.date.today())).values(
                                            'cita').distinct() 

        club_citas = ClubCita.objects.filter(club=obj_club).values('cita').distinct()
        citas = []

        for c in club_citas:
            citas.append(Cita.objects.get(pk=c['cita']))

        citas_pendientes = []

        for c in club_citas_pendientes:
            citas_pendientes.append(Cita.objects.get(pk=c['cita']))

        for cita in citas:
            print(cita.dia.strftime("%Y-%m-%d")+" "+cita.hora_inicio.strftime('%I:%M %p'))
            c = {'id':cita.pk,
            'evento': str(cita.evento),
            # 'club' : str(cita.club),
            'inicio':str(cita.dia.strftime("%Y-%m-%d")+" "+cita.hora_inicio.strftime('%H:%M')), 
            'final':str(cita.dia.strftime("%Y-%m-%d")+" "+cita.hora_fin.strftime('%H:%M')),
            }
            lista_citas.append(c)

        if obj_club:
            context = {
                'club': obj_club.first(),
                'ninos': obj_ninos.all(),
                'facilitadores': obj_facilitadores.all(),
                'clubes': Club.objects.all(),
                'list_ninos': Nino.objects.all(),
                'citas_pendientes': citas_pendientes,
                'citas': json.dumps(lista_citas),
                'form_cita': form
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponse('Invalid request')


class CitasView(TemplateView):
    template_name = 'citas.html'
    def get_context_data(self, **kwargs):
        context = super(CitasView, self).get_context_data(**kwargs)
        form = CitaForm()
        # usuarios = Usuario.objects.filter(role=1)
        context['form_cita'] = form

        if self.request.user.role == 1: #Si es Administrador master
            clubes_pks = Club.objects.all().values_list(
                                            'id', flat=True)

        else: 
            clubes_pks = UsuarioClub.objects.filter(usuario=self.request.user).values_list(
                                            'club', flat=True)

        club_citas = ClubCita.objects.filter(club__pk__in=clubes_pks).values('cita').distinct()
        citas = []

        for c in club_citas:
            citas.append(Cita.objects.get(pk=c['cita']))

        club_citas_pendietes = ClubCita.objects.filter(club__pk__in=clubes_pks,
                                            cita__dia__gte=( datetime.date.today())).values(
                                            'cita').distinct() 
        citas_pendietes = []

        for c in club_citas_pendietes:
            citas_pendietes.append(Cita.objects.get(pk=c['cita']))

        programas_2 = []
        programas = Programa.objects.all()

        for programa in programas:
            clubes = Club.objects.filter(programa = programa,pk__in=clubes_pks)
            if clubes.count()>0:
                programas_2.append({'clubes':clubes,'programa':programa})

        lista_citas = []

        for cita in citas:
            clubes = cita.get_clubes()
            clubes_json = []

            for c in clubes:
                print(c)
                clubes_json.append(c.nombre)

            c = {'id':cita.pk,
            'evento': str(cita.evento),
            'club' : json.dumps(clubes_json),
            'inicio':str(cita.dia.strftime("%Y-%m-%d")+" "+cita.hora_inicio.strftime('%H:%M')), 
            'final':str(cita.dia.strftime("%Y-%m-%d")+" "+cita.hora_fin.strftime('%H:%M')),
            }
            lista_citas.append(c)

        context['citas'] = json.dumps(lista_citas)
        context['citas_pendientes'] = citas_pendietes
        context['programas_clubes'] = programas_2
        # context['citas'] = Cita.objects.filter(club)
        # context['formulario'] = UsuarioForm(instance=None)
        return context

def guardar_cita(request):
    if request.POST:
        club_id = request.POST.get('club_id')
        if club_id:
            club = Club.objects.get(pk=club_id)
            cita = CitaClubForm(request.POST)

            if cita.is_valid():
                cita.save(club=club)
                return HttpResponse(1)
        else:
            cita = CitaForm(request.POST)
            if cita.is_valid():
                clubes_id = request.POST.getlist('club')
                clubes = Club.objects.filter(pk__in=clubes_id)
                cita.save(clubes=clubes)
                return HttpResponse(1)

        print(cita.errors)
        return HttpResponse(0)
    return HttpResponse(0)

def eliminar_cita(request):
    if request.POST:
        id_cita = request.POST.get('id_cita')
        try:
            cita = Cita.objects.get(pk=id_cita)
            cita.delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

def save_club(request):
    if request.POST:
        club = ClubForm(request.POST)
        if club.is_valid():
            club_new = club.save()
            usuario= Usuario.objects.get(usuario=request.user.usuario)
            usuario_club = UsuarioClub.objects.create(club=club_new, usuario=usuario, estado='1')
            return HttpResponse(1)
        else:
            return HttpResponse(0)


def delete_club(request):
    if request.POST:
        id_club = request.POST.get('id_club')
        try:
            club = Club.objects.get(pk=id_club)
            club.delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

def delete_nino_club(request):
    if request.POST:
        id_nino = request.POST.get('id_nino')
        try:
            nino_club = NinoClub.objects.get(pk=id_nino)
            nino_club.delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

def delete_facilitador_club(request):
    if request.POST:
        id_facilitador = request.POST.get('id_facilitador')
        try:
            usuario_club = UsuarioClub.objects.get(pk=id_facilitador)
            usuario_club.delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

            
def edit_club(request):
    if request.method == 'POST':
        id_club = request.POST.get('id_club')
        club= Club.objects.get(pk=id_club)
        form = ClubForm(instance=club)
        return render(request, 'editar_club.html', {
            'formulario': form,
            'id_club':id_club
            })
    else:
        mensaje = "cero"
        return HttpResponse(mensaje, content_type='application/json')

def save_edit_club(request):
    if request.method == 'POST':
        club = Club.objects.get(pk=request.POST.get('id_club'))
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            club = form.save()
            return HttpResponse(1)
        else:
            return HttpResponse(0)
def validate_nino(request):
    if request.POST:
        codigo = request.POST.get('codigo')
        id_club = request.POST.get('id_club')
        valido = Nino.objects.filter(cod_apadr__iexact=codigo).exists()
        club=Club.objects.get(pk=id_club)
        if valido==1:
            nino = Nino.objects.get(cod_apadr=codigo)
            valido_club = NinoClub.objects.filter(nino=nino).filter(club=club).exists()
            if valido_club==1:
               return HttpResponse(2)
            else:
                fecha = datetime.date.today()
                nino_club = NinoClub.objects.create(nino=nino,club=club, fecha=fecha,estado='1',ahorro='0')
                return HttpResponse(1)
        else:
            return HttpResponse(0)

def validate_facilitador(request):
    if request.POST:
        username = request.POST.get('username')
        id_club = request.POST.get('id_club')
        valido = Usuario.objects.filter(usuario__iexact=username).exists()
        club=Club.objects.get(pk=id_club)
        if valido==1:
            usuario= Usuario.objects.get(usuario=username)
            valido_club = UsuarioClub.objects.filter(usuario=usuario).filter(club=club).exists()
            if valido_club==1:
               return HttpResponse(2)
            else:
                usuario_club = UsuarioClub.objects.create(club=club, usuario=usuario, estado='1')
                return HttpResponse(1)
        else:
            return HttpResponse(0)

class TransferenciaView(View):
    template_name = 'transferencia_club.html'
    def get(self, request, club):
        obj_club = Club.objects.get(slug=club)
        obj_ninos = NinoClub.objects.filter(club=obj_club)
        obj_facilitadores = UsuarioClub.objects.filter(club=obj_club)

        if obj_club:
            context = {
                'club': obj_club,
                'ninos': obj_ninos.all(),
                'facilitadores': obj_facilitadores.all(),
                'clubes': Club.objects.exclude(nombre=obj_club.nombre),
                'list_ninos': Nino.objects.all(),
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponse('Invalid request')



def transferencia_nino(request):
    list_ninos=[]
    if request.POST:
        try:
            club_actual = request.POST.get('club_actual')
            club_destino=request.POST.get('club_destino')
            list_ninos=request.POST.getlist('lista_ninos[]')
            club_destino_transferir=Club.objects.get(nombre=club_destino)
            fecha = datetime.date.today()
            for nino in list_ninos:
                nino_actual=NinoClub.objects.get(pk=nino)
                nino_transferible=Nino.objects.get(cod_apadr=nino_actual.nino.cod_apadr)
                nino_club_transferido = NinoClub.objects.create(nino=nino_transferible,club=club_destino_transferir, fecha=fecha,estado=nino_actual.estado,ahorro=nino_actual.ahorro)
                nino_actual.delete()
       

            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)
