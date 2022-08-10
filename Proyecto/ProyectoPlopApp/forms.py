from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ProyectoPlopApp.models import *
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin



class EventoForm(forms.ModelForm):
    imagen = forms.ImageField(label='Flyer(800x500)',required=True)
    fecha = forms.DateField(label='Fecha Inicio(dd/mm/yyyy)')
    hora = forms.TimeField(label='Hora Inicio(hh:mm:ss)')
    class Meta:
        model = Evento
        fields = '__all__'
    

class EventoEditForm(forms.ModelForm):
    imagen = forms.ImageField(label='Flyer(800x500)',required=False)
    fecha = forms.DateField(label='Fecha Inicio(dd/mm/yyyy)')
    hora = forms.TimeField(label='Hora Inicio(hh:mm:ss)')
    class Meta:
        model = Evento
        fields = '__all__'

class FondoPaginaForm(forms.ModelForm):
    imagen = forms.ImageField(label='Imagen()',required=True)
    class Meta:
        model = FondoPagina
        fields = ['nombre','imagen']
