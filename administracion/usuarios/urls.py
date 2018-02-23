try:
	from django.conf.urls import patterns, url
except Exception as e:
	from django.conf.urls import *

from usuarios.views import *
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from .viewsets import *
router = DefaultRouter()
router.register(r'ninos',NinoViewSet)



urlpatterns = [
	url(r'^$', Login.as_view(), name="login"),     
	url(r'^facilitator', login_required(views.FacilitatorView.as_view()), name='facilitator'), 
	url(r'^administrator', login_required(views.AdministratorView.as_view()), name='administrator'),
	url(r'^guardar_facilitador', views.save_facilitator, name='guardar_facilitador'), 
	url(r'^guardar_administrador', views.save_administrator, name='guardar_administrador'),   
	url(r'^eliminar_administrador', views.delete_administrator, name='eliminar_administrador'),
	url(r'^editar_administrador', views.edit_administrator, name='editar_administrador'),   
	url(r'^guardar_cambio_administrador', views.save_edit_administrator, name='guardar_cambio_administrador'),     
    url(r'^guardar_nino', views.save_nino, name='guardar_nino'),
    url(r'^editar_nino',login_required(views.edit_nino), name='editar_nino'), 
    url(r'^guardar_cambio_nino',login_required(views.save_edit_nino), name='guardar_cambio_nino'),
    url(r'^eliminar_club', login_required(views.delete_nino), name='eliminar_nino'),
    url(r'^children', login_required(views.NinosView.as_view()), name='children'),
	url(r'^api/', include(router.urls)),
	url(r'^api/ninoauth/', NinoAuth.as_view())

]
