# -*- coding:utf8 -*-
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):

    user = forms.CharField(label= 'Nombre de Usuario')
    pwd = forms.CharField(label= 'Contraseña', widget=forms.PasswordInput)


class Registrationform(forms.ModelForm):

    class Meta:
        user_django = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
