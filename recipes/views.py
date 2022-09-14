from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render 
# lê e renderiza o arquivo (deixa aparecer no código fonte o HTML, etc)

# Create your views here.

def home(request):
    return render(request, 'recipes/home.html') 
    # adicionar a pasta em q está o arquivo p não haver colisões

def contato(request):
    return render(request, 'me-apague/temp.html')

def sobre(request):
    return HttpResponse('sobreeeee')
