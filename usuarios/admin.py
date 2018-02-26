from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *




#admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
admin.site.register(Usuario)
admin.site.register(UsuarioClub)
admin.site.register(Nino)
admin.site.register(NinoClub)
admin.site.register(Casa)
admin.site.register(Actividad)

