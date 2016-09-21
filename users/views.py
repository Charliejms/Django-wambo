from django.shortcuts import render

# Create your views here.


def login_view(request):

    render(request, 'form.html', {})


def register_view(request):

    render(request, 'register.html', {})


def logout_view(request):
    render(request, 'form.html', {})
