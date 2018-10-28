from django import forms

class LoginForm(forms.Form):
    usuario = forms.CharField(label='usuario', max_length=15)
    contrasenia = forms.CharField(widget=forms.PasswordInput)
    widgets = {
            'contrasenia': forms.PasswordInput(),
        }