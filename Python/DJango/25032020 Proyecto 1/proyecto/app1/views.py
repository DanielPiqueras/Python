from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from .models import Persona

from .forms import AnyadirFormulario

from django.views.decorators.http import require_POST

def index(request):
    template = loader.get_template('app1/index.html')

    return HttpResponse(template.render())

def mostrar(request):
    template = loader.get_template('app1/mostrar.html')

    personas = Persona.objects.all()

    context = {
        'personas' : personas,
    }

    return HttpResponse(template.render(context, request))

def formulario_anyadir(request):
    template = loader.get_template('app1/formulario.html')

    form = AnyadirFormulario()

    context = {
        'form' : form
    }

    return HttpResponse(template.render(context, request))


@require_POST
def anyadir(request):
 
    form = AnyadirFormulario(request.POST)

    print(f"El nombre que desea introducir es: {request.POST['nombre']} y su edad {request.POST['edad']}")

    if form.is_valid():
        nueva_persona = Persona(nombre = request.POST['nombre'], edad = request.POST['edad'])
        nueva_persona.save()

    return redirect('index')

def borrar(request, persona_id):

    print(f"La id de esta persona es {persona_id}")

    Persona.objects.filter(id=persona_id).delete()

    return redirect('mostrar')

def borrar_todo(request):

    Persona.objects.all().delete()

    return redirect('index')
