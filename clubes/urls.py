from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.ClubesView.as_view()), name='clubes'),
    url(r'^(?P<club>[\w\-]+)/$', login_required(views.ClubView.as_view()), name='club'),
    url(r'^editar_club',login_required(views.edit_club), name='editar_club'), 
    url(r'^guardar_cambio_club',login_required(views.save_edit_club), name='guardar_cambio_club'),
    url(r'^eliminar_club', login_required(views.delete_club), name='eliminar_club'),
    url(r'^citas', login_required(views.CitasView.as_view()), name='citas'),
    url(r'^guardar_cita', views.guardar_cita, name='guardar_cita'),
    url(r'^eliminar_cita', views.eliminar_cita, name='eliminar_cita'),
    url(r'^eliminar_nino_club', views.delete_nino_club, name='eliminar_nino_club'),
    url(r'^eliminar_facilitador_club', views.delete_facilitador_club, name='eliminar_facilitador_club'),
    url(r'^validate_nino', views.validate_nino, name='validate_nino'),
    url(r'^validate_facilitador', views.validate_facilitador, name='validate_facilitador'),
    url(r'^guardar_club', views.save_club, name='guardar_club'),
    url(r'^transferencia_club/(?P<club>[\w\-]+)/$', login_required(views.TransferenciaView.as_view()), name='transferencia_club'),
    url(r'^transferencia_nino', views.transferencia_nino, name='transferencia_nino'),

]
