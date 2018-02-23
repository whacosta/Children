from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.ProgramsView.as_view()), name='programs'),
    # url(r'^programita$', views.ProgramaView.as_view(), name='programa'),
    url(r'^(?P<programa>[\w\-]+)/$', views.ProgramaView.as_view(), name='programa'),
    url(r'^(?P<programa>[\w\-]+)/elemento/(?P<elemento_clave>[\w\-]+)/$', views.ElementoClaveView.as_view(), name='elemento_clave'),
    url(r'^(?P<programa>[\w\-]+)/elemento/(?P<elemento_clave>[\w\-]+)/casa/(?P<casa>[\w\-]+)/$', views.CasaView.as_view(), name='casa'),
    url(r'^(?P<programa>[\w\-]+)/elemento/(?P<elemento_clave>[\w\-]+)/casa/(?P<casa>[\w\-]+)/actividad/(?P<actividad>[\w\-]+)/$', views.RecursoActividadView.as_view(), name='recurso_actividad'),
    url(r'^(?P<programa>[\w\-]+)/actividad/(?P<actividad>[\w\-]+)/$', views.ActividadesView.as_view(), name='actividad'),
    url(r'^guardar_elemento_clave', views.save_elemento_clave, name='guardar_elemento_clave'),
    url(r'^eliminar_elemento_clave', views.delete_elemento_clave, name='eliminar_elemento_clave'),
    url(r'^guardar_ubicacion_implementacion', views.save_ubicacion_implementacion, name='guardar_ubicacion_implementacion'),
    url(r'^eliminar_ubicacion_implementacion', views.delete_ubicacion_implementacion, name='eliminar_ubicacion_implementacion'),
    url(r'^guardar_resultado_aprendizaje', views.save_resultado_aprendizaje, name='guardar_resultado_aprendizaje'),
    url(r'^eliminar_resultado_aprendizaje', views.delete_resultado_aprendizaje, name='eliminar_resultado_aprendizaje'),
    url(r'^guardar_casa', views.save_casa, name='guardar_casa'),
    url(r'^eliminar_casa', views.delete_casa, name='eliminar_casa'),
    url(r'^eliminar_tienda', views.delete_tienda, name='eliminar_tienda'),
    url(r'^eliminar_recurso_clave', views.delete_recurso_clave, name='eliminar_recurso_clave'),
    url(r'^guardar_actividad', views.save_actividad, name='guardar_actividad'),
    url(r'^eliminar_actividad', views.delete_actividad, name='eliminar_actividad'),
    url(r'^eliminar_recurso_casa', views.delete_recurso_casa, name='eliminar_recurso_casa'),
    url(r'^eliminar_recurso_actividad', views.delete_recurso_actividad, name='eliminar_recurso_actividad'),
]


