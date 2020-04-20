from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('formulario_editar/<contacto_id>', views.formulario_editar, name='formulario_editar'),
]