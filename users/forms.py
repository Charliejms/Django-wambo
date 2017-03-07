# -*- coding:utf8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout, get_user_model


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='User name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwarg):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exits')
            if not user.check_password(password):
                raise forms.ValidationError('Incprrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active.')
        return super(UserLoginForm, self).clean(*args, **kwarg)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address', required=True)
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get(('email2'))
        if email != email2:
            raise forms.ValidationError('Emails must match')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email has already been register')
        return super(UserRegisterForm, self).clean(*args, **kwargs)

    # def clean_email2(self):
    #     email = self.cleaned_data.get('email')
    #     email2 = self.cleaned_data.get(('email2'))
    #     if email != email2:
    #         raise forms.ValidationError('Emails must match')
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise forms.ValidationError('This email has already been register')
    #     return email


class LoginForm(forms.Form):
    user = forms.CharField(label= 'Nombre de Usuario')
    pwd = forms.CharField(label= 'Contraseña', widget=forms.PasswordInput)


class Registrationform(forms.Form):

    class Meta:
        user_django = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
