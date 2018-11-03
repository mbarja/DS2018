from django import forms
from .models import *
from django.forms import ModelForm, Textarea, Select
from django.forms.widgets import Select

class LoginForm(forms.Form):
    usuario = forms.CharField(label='usuario', max_length=15)
    contrasenia = forms.CharField(widget=forms.PasswordInput)
    widgets = {
            'contrasenia': forms.PasswordInput(),
        }
    
class EquipoForm(forms.ModelForm):

    class Meta:
        model = Equipo
        fields = '__all__'
        widgets = {
            'nombre': Textarea(attrs={'cols': 10, 'rows': 1}),
            'unidad_medida': Select()
        }
        