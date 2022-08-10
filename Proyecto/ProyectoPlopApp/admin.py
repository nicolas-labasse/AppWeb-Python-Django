from django.contrib import admin
from.models import *
# Register your models here.


class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'hora', 'lugar', 'imagen', 'link_compra')
    list_filter = ('fecha', 'hora', 'lugar')
    search_fields = ('titulo', 'lugar')


class FondoPaginaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'aprobado', 'imagen')
    list_filter = ('aprobado',)
    search_fields = ('nombre',)

admin.site.register(Evento, EventoAdmin)
admin.site.register(FondoPagina, FondoPaginaAdmin)





