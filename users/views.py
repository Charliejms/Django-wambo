# Create your  User-views here.

from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LoginForm, Registrationform, UserRegisterForm
from .forms import UserLoginForm


class LoginView(View):

    def get(self, request):
        """
        Presenta el formulario de login
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        error_message = ""
        login_form = LoginForm()
        context = {'error': error_message, 'form': login_form}
        return render(request, 'users/login.html', context)

    def post(self, request):
        """
        Gestiona el login de un usuario
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        error_message = ""
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('pwd')
            user = authenticate(username=username, password=password)
            if user is None:
                error_message = "Usuario o contraseña incorrecto"
            else:
                if user.is_active:
                    django_login(request, user)
                    return redirect(request.GET.get('next', 'photos_home'))
                else:
                    error_message = "Cuenta de usuario inactiva"
        context = {'error': error_message, 'form': login_form}
        return render(request, 'users/login.html', context)


class LogoutView(View):

    def get(self, request):
        """
        Hace el logout de un usuario y redirige al login
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        if request.user.is_authenticated():
            django_logout(request)
        return redirect('photos_home')


class RegisterView(View):

    def get(self, request):
        register_form = Registrationform()
        context ={
            'form': register_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        register_form = Registrationform(request.POST)
        if register_form.is_valid():
            first_name = register_form.cleaned_data.get('first-name')
            last_name = register_form.cleaned_data.get('last_name')
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
        return render()


def login_view(request):
    """
    Gestiona el login del Usuario
    :param request: objeto HttpRequest con los datos de la petición
    :return: objeto Httpresponse con los datos de la respuesta
    """
    next = request.GET.get('next')
    title = 'Login'
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        django_login(request, user)
        if next:
            return redirect(next)
        #redirect
        return redirect('url_post_list')
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'users/login.html', context)


def register_view(request):
    """
    Gestiona el registro del usuario
    :param request: objeto HttpRequeste con los datos de la petición
    :return: objeto HttpResponse con los datos de la respuesta
    """
    next = request.GET.get('next')
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        django_login(request, new_user)
        if next:
            return redirect(next)
        # redirect
        return redirect('url_post_list')

    context = {
        'form': form,
        'title': title
    }

    return render(request, 'users/register.html', context)


def logout_view(request):
    """
    Gestiona el logout del Usuario
    :param request: objeto HttpRequest con los parametros de la petición
    :return: objeto HttpResponse con los parametros de la respuesta
    """
    django_logout(request)
    return redirect('url_post_list')
    #return render(request, 'users/logout.html', {})
