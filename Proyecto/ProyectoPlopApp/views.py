import datetime
from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect, render
import requests
from ProyectoPlopApp.forms import *
from ProyectoPlopApp.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


# Create your views here.

def inicio(request):
    url = " /media/imagenes/fiesta.png"
    fondo = FondoPagina.objects.all()
    if len(fondo) > 0:
     url_fondo = FondoPagina.objects.get(aprobado = True)
    else:
     url_fondo = FondoPagina.objects.create(
        nombre = 'Default',
        aprobado = True,
        imagen = "/imagenes/1.jpeg",
     )
     url_fondo.save()
    buscar = request.GET.get('buscar')
    page = request.GET.get('page', 1)
    numero = 1
    if buscar is not None and buscar is not "":
        buscador = Evento.objects.filter(Q(titulo__icontains=buscar)  | Q(lugar__icontains=buscar) | Q(fecha__icontains=buscar) | Q(hora__icontains=buscar))
        paginator = Paginator(buscador, 2)
        buscador = paginator.page(page)
        return render(request, 'ProyectoPlopApp/index.html', {'buscador': buscador, 'paginator': paginator, 'buscar': buscar, 'url': url, 'url_fondo': url_fondo,'numero':numero})
    else:
        eventos = Evento.objects.filter(fecha__gte=datetime.datetime.now())
        paginas = len(eventos)/6
        paginas = int(paginas)
        numero = 1
        if numero == 1:
            numero = numero + 1
            eventos = eventos[:6]
        else:
            numero = numero
    return render (request, 'ProyectoPlopApp/index.html', {'eventos': eventos, 'url': url,'paginas':paginas,'numero':numero, 'url_fondo': url_fondo})

@staff_member_required
def panel(request,tab):
    buscar = request.GET.get('buscar')
    page = request.GET.get('page', 1)
    if tab == 'evento':
        if buscar is not None and buscar is not "":
            buscador = Evento.objects.filter(Q(titulo__icontains=buscar)  | Q(lugar__icontains=buscar) | Q(fecha__icontains=buscar) | Q(hora__icontains=buscar) )
            paginator = Paginator(buscador, 2)
            buscador = paginator.page(page)
            return render(request, 'ProyectoPlopApp/panel.html', {'buscador': buscador, 'paginator': paginator, 'buscar': buscar, 'tab': tab})
        else:
            eventos = Evento.objects.all()
            paginator = Paginator(eventos, 6)
            eventos = paginator.page(page)
            return render (request, 'ProyectoPlopApp/panel.html', {'eventos': eventos, 'paginator': paginator, 'tab': tab})
    else:
        if buscar is not None and buscar is not "":
            buscador = FondoPagina.objects.filter(Q(nombre__icontains=buscar))
            paginator = Paginator(buscador, 2)
            buscador = paginator.page(page)
            return render(request, 'ProyectoPlopApp/panel.html', {'buscador': buscador, 'paginator': paginator, 'buscar': buscar, 'tab': tab})
        else:
            fondos = FondoPagina.objects.all()
            paginator = Paginator(fondos, 6)
            fondos = paginator.page(page)
            return render (request, 'ProyectoPlopApp/panel.html', {'fondos': fondos, 'paginator': paginator, 'tab': tab})

@staff_member_required
def eliminar_evento(request, evento_id):
    eventos = Evento.objects.get(id=evento_id)
    eventos.delete()
    messages.add_message(request, messages.SUCCESS, 'El Evento ha sido eliminado correctamente')
    return redirect('/panel/evento')

@staff_member_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            info_form = form.cleaned_data
            evento = Evento.objects.create(titulo=info_form['titulo'], fecha=info_form['fecha'], hora=info_form['hora'], lugar=info_form['lugar'], imagen=info_form['imagen'], link_compra=info_form['link_compra'])
            evento.save()
            messages.add_message(request, messages.SUCCESS, 'El Evento ha sido creado correctamente')
            return redirect('/panel/evento')
        else:
            messages.add_message(request, messages.ERROR, 'El Evento no ha sido creado correctamente, ingreso mal la fecha o la hora')
            return redirect('/panel/evento')
    else:
        form = EventoForm()
        url_fondo = FondoPagina.objects.get(aprobado = True)
        return render(request, 'ProyectoPlopApp/crear_evento.html', {'form': form, 'url_fondo': url_fondo})

@staff_member_required
def editar_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    if request.method == 'POST':
        form = EventoEditForm(request.POST, request.FILES)
        if form.is_valid():
            info_form = form.cleaned_data
            evento.titulo = info_form['titulo']
            evento.fecha = info_form['fecha']
            evento.hora = info_form['hora']
            evento.lugar = info_form['lugar']
            evento.imagen = info_form['imagen']
            evento.link_compra = info_form['link_compra']
            evento.save()
            messages.add_message(request, messages.SUCCESS, 'El Evento ha sido editado correctamente')
            return redirect('/panel/evento')
    else:
        form = EventoEditForm(initial={'titulo': evento.titulo, 'fecha': evento.fecha, 'hora': evento.hora, 'lugar': evento.lugar, 'imagen': evento.imagen, 'link_compra': evento.link_compra})
    return render(request, 'ProyectoPlopApp/editar_evento.html', {'form': form, 'evento': evento})


def contacto_email(request):
  if request.method == "POST":
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = 'Contacto desde la web'
    message = request.POST.get('message')

    template = render_to_string('ProyectoPlopApp/contacto_email.html', {
        'name': name,
        'email': email,
        'subject': subject,
        'message': message
    })
    email = EmailMessage(
        subject,
        template,
        settings.EMAIL_HOST_USER,
        ['nicolaslabasse4@gmail.com']
    )
    email.fail_silently = False
    email.send()
    messages.success(request, 'Mensaje enviado correctamente.')
    return redirect('inicio')

@staff_member_required
def agregar_imagenes(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    evento.detalle = True
    evento.save()
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for img in images:
            ImagenesEvento.objects.create(images=img, evento = evento)
        return redirect('/panel/evento')
    else:
        return render(request, 'ProyectoPlopApp/agregar_imagenes.html')

def eliminar_imagen(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    evento.detalle = False
    evento.save()
    images = ImagenesEvento.objects.filter(evento=evento)
    for img in images:
     img.delete()
    return redirect('/panel/evento')

def detalle_evento(request, evento_id):
    url = " /media/imagenes/fiesta.png"
    evento = Evento.objects.get(id=evento_id)
    images = ImagenesEvento.objects.filter(evento = evento)
    url_fondo = FondoPagina.objects.get(aprobado = True)
    return render(request, 'ProyectoPlopApp/detalle_evento.html', { 'images': images, 'url_fondo': url_fondo,'url': url})

@staff_member_required
def eliminar_fondo(request, fondo_id):
    fondo = FondoPagina.objects.get(id=fondo_id)
    fondo.delete()
    messages.add_message(request, messages.SUCCESS, 'El Fondo ha sido eliminado correctamente')
    return redirect('/panel/fondo')


@staff_member_required
def aprobar_fondo(request, fondo_id):
    fondos = FondoPagina.objects.all()
    for f in fondos:
        f.aprobado = False
        f.save()
    fondo = FondoPagina.objects.get(id=fondo_id)
    fondo.aprobado = True
    fondo.save()
    messages.add_message(request, messages.SUCCESS, 'El Fondo ha sido aprobado correctamente')
    return redirect('/panel/fondo')

@staff_member_required
def crear_fondo(request):
    if request.method == 'POST':
        form = FondoPaginaForm(request.POST, request.FILES)
        if form.is_valid():
            info_form = form.cleaned_data
            fondo = FondoPagina.objects.create(nombre=info_form['nombre'], imagen=info_form['imagen'], aprobado=False)
            fondo.save()
            messages.add_message(request, messages.SUCCESS, 'El Fondo ha sido creado correctamente')
            return redirect('/panel/fondo')
    else:
        form = FondoPaginaForm()
        url_fondo = FondoPagina.objects.get(aprobado = True)
    return render(request, 'ProyectoPlopApp/crear_fondo.html', {'form': form, 'url_fondo': url_fondo})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("inicio")
            else:
               return redirect("login")
        else:
            return redirect("login")

    form = AuthenticationForm()
    url_fondo = FondoPagina.objects.get(aprobado = True)

    return render(request, 'ProyectoPlopApp/login.html', {'form': form, 'url_fondo': url_fondo})


@staff_member_required
def logout_request(request):
    logout(request)
    return redirect("inicio")




def home(request, numero):
    url = " /media/imagenes/fiesta.png"
    url_fondo = FondoPagina.objects.get(aprobado = True)
    buscar = request.GET.get('buscar')
    page = request.GET.get('page', 1)
    if buscar is not None and buscar is not "":
        buscador = Evento.objects.filter(Q(titulo__icontains=buscar)  | Q(lugar__icontains=buscar) | Q(fecha__icontains=buscar) | Q(hora__icontains=buscar) )
        paginator = Paginator(buscador, 2)
        buscador = paginator.page(page)
        return render(request, 'ProyectoPlopApp/index.html', {'buscador': buscador, 'paginator': paginator, 'buscar': buscar, 'url': url, 'url_fondo': url_fondo, 'numero': numero})
    else:
        if numero == 2:
            #eventos = Evento.objects.all().order_by('-id')
            #eventos = Evento.objects.all().order_by('-fecha')[:6]
            eventos = Evento.objects.all()[:6]
            paginas = len(eventos)/6
            paginas = int(paginas)
            numero = numero + 1
        else:
            #eventos = Evento.objects.all().order_by('-id')[:6*numero]
            eventos = Evento.objects.all()[:6*numero]
            paginas = len(eventos)/6
            paginas = int(paginas)
            numero = numero + 1
        return render (request, 'ProyectoPlopApp/index.html', {'eventos': eventos, 'url': url,'paginas':paginas,'numero':numero, 'url_fondo': url_fondo})

def test(request):
    return render(request, 'ProyectoPlopApp/test.html')