from django import forms
from .models import *
from django.forms import ModelForm, Textarea, Select, TextInput
from django.forms.widgets import Select
from dataclasses import fields

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
        
        
class TratamientoForm(forms.ModelForm):

    class Meta:
        model = Tratamiento
        fields = '__all__'
        widgets = {
            'nombre': Textarea(attrs={'cols': 20, 'rows': 1}),
            'informacion': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        equipo = forms.ModelChoiceField(queryset=Equipo.objects.all())
        
class TecnicoForm(forms.ModelForm):
    
    class Meta:
        model = Tecnico
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'dni': TextInput(attrs={'placeholder': 'DNI', 'class': 'form-control'}),
            'mail': TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'direccion': TextInput(attrs={'placeholder': 'Direccion', 'class': 'form-control'}),
            'telefono': TextInput(attrs={'placeholder': 'Telefono', 'class': 'form-control'}),
            'usuario': TextInput(attrs={'placeholder': 'Usuario', 'class': 'form-control'}),
            'contrasenia': TextInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        }

class PrecioUsoForm(forms.ModelForm):
    
    class Meta:
        model = PrecioPorUso
        fields = '__all__'
        equipo = forms.ModelChoiceField(queryset=Equipo.objects.all())
        


class AlquilerForm(forms.Form):
    
    equipos = forms.ModelChoiceField(queryset=Equipo.objects.all())
    fechas = forms.CharField(label='Rango de fechas', max_length=35)
    widgets = {
            'fechas': TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control', 'id':'fechas', 'name':'datetimes'}),
    }