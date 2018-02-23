from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import Programa
from .models import ElementoClave
from .models import Recurso
from .models import Ubicacionimplementacion
from .models import Casa
from clubes.models import Club
from usuarios.models import Actividad,ActividadNino
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
class ProgramsView(View):
    template_name = 'programas.html'

    def get(self, request):
        context = {
            'programas': Programa.objects.all()
        }
        return render(request,self.template_name, context)

    def post(self, request):
        print(request.POST)
        nombre = request.POST.get('nombre', None)
        icono = request.POST.get('icono', None)
        edad_ini = request.POST.get('edad_ini', None)
        edad_fin= request.POST.get('edad_fin', None)
        objetivo= request.POST.get('objetivo', None)
        tipo= request.POST.get('tipo', None)
        if nombre != None and icono != None:
            programa = Programa.objects.create(nombre=nombre, edad_ini=edad_ini, edad_fin=edad_fin, tipo=tipo, objetivo=objetivo, imagen=icono)
            return redirect('programs')
        else:
            return redirect('programs')



class ProgramaView(View):
    template_name = 'programa.html'
    def get(self, request, programa):
        # try:
        club_by_user= []
        obj_programa = Programa.objects.get(slug=programa)
        ct = ContentType.objects.get_for_model(obj_programa)
        lista = UsuarioClub.objects.filter(usuario__usuario=request.user.usuario).only('usuario', 'club')
        for variable in lista:
            club=Club.objects.get(nombre=variable.club)
            club_by_user.append(club)
        if obj_programa:
            context = {
                'formulario_elemento': ElementoClaveForm(instance=None),
                'form': RecursoClaveForm(),
                'programas': Programa.objects.all(), #all programs
                'programa': obj_programa,   #program to show
                'elementos_clave': obj_programa.elementos_clave.all(), #elementos clave from program
                'clubes': club_by_user, #clubes from program
                'recursos_claves': Recurso.objects.filter(content_type=ct, content_id=obj_programa.pk),
                'ubicaciones':Ubicacionimplementacion.objects.filter(programa=obj_programa)
            }
            return render(request, self.template_name, context)
        else:
             return HttpResponse('Invalid request')
    def post(self, request,programa):
        object_programa= Programa.objects.get(slug=programa)
        form = RecursoClaveForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_recurso=form.save(commit=False)
            nuevo_recurso.content=object_programa
            nuevo_recurso.save()
            return redirect('programa',programa=programa)
        else:
            return redirect('programa',programa=programa)


class ElementoClaveView(View):
    template_name = 'elemento_clave.html'
    def get(self, request, programa, elemento_clave):
        obj_programa = Programa.objects.get(slug=programa)
        obj_elemento = ElementoClave.objects.get(slug=elemento_clave)
        context = {
            'formulario_resultado': ResultadoAprendizajeForm(instance=None),
            'formulario_casa': CasaForm(instance=None),
            'form': TiendaForm(),
            'programas': Programa.objects.all(),
            'casas': obj_elemento.casas.all(),
            'resultados' : obj_elemento.resultados_aprendizaje.all(),
            'tienda' : obj_elemento.personalidades.all(),
            'programa': obj_programa,
            'elemento': obj_elemento,
        }
        return render(request, self.template_name, context)

    def post(self, request,programa, elemento_clave):
        object_elemento= ElementoClave.objects.get(slug=elemento_clave)
        form = TiendaForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_personalidad=form.save(commit=False)
            nueva_personalidad.elemento_clave=object_elemento
            nueva_personalidad.save()
            return redirect('elemento_clave',programa=programa,elemento_clave=elemento_clave)
        else:
            return redirect('elemento_clave',programa=programa,elemento_clave=elemento_clave)


class ActividadesView(View):
    # Recursos por alguna razon tambien es actividades, no se no entiendo :/
    template_name = 'actividades.html'
    def get(self, request, programa, actividad):
        obj_programa = Programa.objects.get(slug=programa)
        obj_actividad = Recurso.objects.get(slug=actividad)
        context = {
            'programas': Programa.objects.all(),
            'programa': obj_programa,
            'recurso': obj_actividad
        }
        return render(request, self.template_name, context)

class CasaView(View):
    template_name = 'casa.html'
    def get(self, request, programa, elemento_clave, casa):
        obj_programa = Programa.objects.get(slug=programa)
        obj_elemento = ElementoClave.objects.get(slug=elemento_clave)
        obj_casa = Casa.objects.get(slug=casa)
        ct = ContentType.objects.get_for_model(obj_casa)
        context = {
            'programa': obj_programa,
            'form': RecursoClaveForm(),
            'elemento': obj_elemento,
            'casa': obj_casa,
            'recursos_claves': Recurso.objects.filter(content_type=ct, content_id=obj_casa.pk),
            'actividades':obj_casa.actividades.all(),

        }
        return render(request, self.template_name, context)

    def post(self, request,programa, elemento_clave, casa):
        object_casa= Casa.objects.get(slug=casa)
        form = RecursoClaveForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_recurso=form.save(commit=False)
            nuevo_recurso.content=object_casa
            nuevo_recurso.save()
            return redirect('casa',programa=programa,elemento_clave=elemento_clave, casa=casa)
        else:
            return redirect('casa',programa=programa,elemento_clave=elemento_clave, casa=casa)

class RecursoActividadView(View):
    template_name = 'recursoActividad.html'
    def get(self, request, programa, elemento_clave, casa, actividad):
        obj_programa = Programa.objects.get(slug=programa)
        obj_elemento = ElementoClave.objects.get(slug=elemento_clave)
        obj_casa = Casa.objects.get(slug=casa)
        obj_actividad = Actividad.objects.get(slug=actividad)
        ct = ContentType.objects.get_for_model(obj_actividad)
        context = {
            'programa': obj_programa,
            'form': RecursoClaveForm(),
            'elemento': obj_elemento,
            'casa': obj_casa,
            'actividad': obj_actividad,
            'recursos_claves': Recurso.objects.filter(content_type=ct, content_id=obj_actividad.pk),

        }
        return render(request, self.template_name, context)

    def post(self, request,programa, elemento_clave, casa, actividad):
        object_actividad= Actividad.objects.get(slug=actividad)
        form = RecursoClaveForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_recurso=form.save(commit=False)
            nuevo_recurso.content=object_actividad
            nuevo_recurso.save()
            return redirect('recurso_actividad',programa=programa,elemento_clave=elemento_clave, casa=casa, actividad=actividad)
        else:
            return redirect('recurso_actividad',programa=programa,elemento_clave=elemento_clave, casa=casa, actividad=actividad)
        
def save_elemento_clave(request):
    if request.POST:
        name_program=request.POST.get('programa')
        programa= Programa.objects.get(nombre=name_program)
        elemento = ElementoClaveForm(request.POST)
        if elemento.is_valid():
           elemento_new = elemento.save(commit=False)
           elemento_new.programa=programa
           ElementoClave.objects.create(programa= elemento_new.programa, nombre=elemento_new.nombre,orden=elemento_new.orden,color=elemento_new.color)
           return HttpResponse(1)
        else:
            return HttpResponse(0)
    

def delete_elemento_clave(request):
      if request.POST:
        try:
            ElementoClave.objects.filter(id__in=request.POST.getlist('lista_elementos[]')).delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

def delete_ubicacion_implementacion(request):
      if request.POST:
        try:
            Ubicacionimplementacion.objects.filter(id__in=request.POST.getlist('lista_ubicaciones[]')).delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

def save_ubicacion_implementacion(request):
    if request.POST:
        name_program=request.POST.get('programa')
        programa= Programa.objects.get(nombre=name_program)
        ciudad= request.POST.get('ciudad', None)
        lat = request.POST.get('latitud', None)
        lon = request.POST.get('longitud', None)
        if ciudad != None and name_program != None:
            ubicacion_new = Ubicacionimplementacion.objects.create(programa=programa, latitud=lat,longitud=lon,ciudad=ciudad)
            return HttpResponse(1)
        else:
            return HttpResponse(0)

def delete_resultado_aprendizaje(request):
      if request.POST:
        try:
            ResultadoDeAprendizaje.objects.filter(id__in=request.POST.getlist('lista_resultados[]')).delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

def save_resultado_aprendizaje(request):
   if request.POST:
        name_elemento=request.POST.get('elemento')
        elemento= ElementoClave.objects.get(nombre=name_elemento)
        resultado = ResultadoAprendizajeForm(request.POST)
        if resultado.is_valid():
           resultado_new = resultado.save(commit=False)
           resultado_new.elemento_clave=elemento
           ResultadoDeAprendizaje.objects.create(elemento_clave= resultado_new.elemento_clave, nivel=resultado_new.nivel,resultado=resultado_new.resultado,orden=resultado_new.orden)
           return HttpResponse(1)
        else:
            return HttpResponse(0)

def delete_casa(request):
      if request.POST:
        try:
            Casa.objects.filter(id__in=request.POST.getlist('lista_casas[]')).delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

def save_casa(request):
   if request.POST:
        name_elemento=request.POST.get('elemento')
        elemento= ElementoClave.objects.get(nombre=name_elemento)
        casa = CasaForm(request.POST)
        if casa.is_valid():
           casa_new = casa.save(commit=False)
           casa_new.elemento_clave=elemento
           Casa.objects.create(mundo= casa_new.elemento_clave, nombre=casa_new.nombre,orden=casa_new.orden)
           return HttpResponse(1)
        else:
            return HttpResponse(0)

def delete_tienda(request):
      if request.POST:
        try:
            Tienda.objects.filter(id__in=request.POST.getlist('lista_tiendas[]')).delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

def save_tienda(request):
   if request.POST:
        name_elemento=request.POST.get('elemento')
        elemento= ElementoClave.objects.get(nombre=name_elemento)
        tienda = TiendaForm(request.POST, request.FILES)
        if tienda.is_valid():
           tienda_new = tienda.save(commit=False)
           tienda_new.elemento_clave=elemento
           tienda_new.save()
           return HttpResponse(1)
        else:
            return HttpResponse(0)

def delete_recurso_clave(request):
      if request.POST:
        try:
            Recurso.objects.filter(id__in=request.POST.getlist('lista_recursos_claves[]')).delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

def save_actividad(request):
    if request.POST:
        name_casa=request.POST.get('casa')
        casa= Casa.objects.get(nombre=name_casa)
        nombre= request.POST.get('nombre', None)
        nivel = request.POST.get('nivel', None)
        orden = request.POST.get('orden', None)
        tipo= request.POST.get('tipo', None)
        premio = request.POST.get('premio', None)
        tiempo_esperado = request.POST.get('tiempo_esperado', None)
        if casa != None and premio != None:
            actividad_new = Actividad.objects.create(casa=casa, nombre=nombre, nivel=nivel, orden=orden, tipo=tipo, premio=premio,tiempo_esperado=tiempo_esperado)
            return HttpResponse(1)
        else:
            return HttpResponse(0)

def delete_actividad(request):
      if request.POST:
        try:
            Actividad.objects.filter(id__in=request.POST.getlist('lista_actividades[]')).delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)

def delete_recurso_casa(request):
      if request.POST:
        try:
            Recurso.objects.filter(id__in=request.POST.getlist('lista_recursos_casa[]')).delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)
    
def delete_recurso_actividad(request):
      if request.POST:
        try:
            Recurso.objects.filter(id__in=request.POST.getlist('lista_recursos_actividad[]')).delete()
            return HttpResponse(1)
        except Exception as e:
            return HttpResponse(0)