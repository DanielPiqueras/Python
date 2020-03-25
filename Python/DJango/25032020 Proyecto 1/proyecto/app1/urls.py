from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mostrar/', views.mostrar, name='mostrar'),
    path('formulario_anyadir/', views.formulario_anyadir, name='formulario_anyadir'),
    path('anyadir/', views.anyadir, name='anyadir'),
    path('borrar/<persona_id>', views.borrar, name='borrar'),
    path('borrar_todo/', views.borrar_todo, name='borrar_todo')
]