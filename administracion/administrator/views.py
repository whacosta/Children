from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from usuarios.models import Nino, NinoClub
from programas.models import Programa
from clubes.models import Club
from django.shortcuts import render_to_response
from django.template import RequestContext

def e_handler400(request):
    context = RequestContext(request)
    response = render_to_response('400.html', context)
    response.status_code = 400
    return response 
 
def e_handler403(request):
    context = RequestContext(request)
    response = render_to_response('403.html', context)
    response.status_code = 403
    return response

def e_handler404(request):
    context = RequestContext(request)
    response = render_to_response('404.html', context)
    response.status_code = 404
    return response
    
def e_handler500(request):
    context = RequestContext(request)
    response = render_to_response('500.html', context)
    response.status_code = 500
    return response
 

class HomeView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['clubes'] = Club.objects.count()
        context['ninos'] = Nino.objects.count()
        context['programas'] = Programa.objects.all()
        context['lista_clubes'] = self.lista_clubes_dashboard()
        return context

    def lista_clubes_dashboard(self):
        lista = []
        for club in Club.objects.all():
                nombre_club = club.nombre
                ninos_club = NinoClub.objects.filter(club=club).count()
                actividades_club = Programa.objects.filter(clubes=club).count()
                lista.append((nombre_club, ninos_club, actividades_club))
        return lista

# class ProfileView(TemplateView):
#     template_name = 'page-profile.html'


class ChildrenView(TemplateView):
    template_name = 'ninos.html'


class ActivitiesView(TemplateView):
    template_name = 'actividades.html'


class AflatounView(TemplateView):
    template_name = 'aflatoun.html'


class AddChildView(TemplateView):
    template_name = 'agregar_nino.html'


class CalendarView(TemplateView):
    template_name = 'calendario.html'


class ProfileView(TemplateView):
    template_name = 'perfil.html'
