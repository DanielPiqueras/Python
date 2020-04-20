from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.decorators.http import require_POST

from .models import Contacto, Categoria

from .forms import Editar

def index(request):

    contactos = Contacto.objects.all()

    context = {
        'contactos' : contactos
    }

    return render(request, 'index.html', context)


def formulario_editar(request, contacto_id):

    form = Editar()

    context = {
        'form': form
    }

    print (contacto_id)
    return render(request, 'editar.html', context)