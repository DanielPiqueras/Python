from django import forms
from .models import Contacto, Categoria

class Editar(forms.Form):
    text = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    phone = forms.CharField(max_length=9)

class newEditar(forms.ModelForm):
    class Meta:
        model = Contacto
