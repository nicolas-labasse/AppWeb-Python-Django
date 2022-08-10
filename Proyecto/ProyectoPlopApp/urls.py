from django import views

from django.urls import path
from ProyectoPlopApp import views


urlpatterns = [
    # URLS de ProyectoPlopApp
path('', views.inicio, name='inicio'),
path('panel/<str:tab>/', views.panel, name='panel'),
path('contacto_email/', views.contacto_email, name='contacto_email'),
# URLS de Eventos
path('eliminar_evento/<evento_id>/', views.eliminar_evento, name='eliminar_evento'),
path('crear_evento/', views.crear_evento, name='crear_evento'),
path('editar_evento/<evento_id>/', views.editar_evento, name='editar_evento'),
path('detalle_evento/<evento_id>/', views.detalle_evento, name='detalle_evento'),
path('agregar_imagenes/<evento_id>/', views.agregar_imagenes, name='agregar_imagenes'),
path('eliminar_imagen/<evento_id>/', views.eliminar_imagen, name='eliminar_imagen'),
# URLS de fondos
path('eliminar_fondo/<fondo_id>/', views.eliminar_fondo, name='eliminar_fondo'),
path('aprobar_fondo/<fondo_id>/', views.aprobar_fondo, name='aprobar_fondo'),
path('crear_fondo/', views.crear_fondo, name='crear_fondo'),

# URL Login
path('login/', views.login_request, name='login'),
path('logout/', views.logout_request, name='logout_request'),
# URL test
path('test/<int:numero>/', views.test, name='test'),
path('home/<int:numero>/', views.home, name='home'),


]