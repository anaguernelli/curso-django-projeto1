from django.shortcuts import render 
# lê e renderiza o arquivo (deixa aparecer no código fonte o HTML, etc)

# Create your views here.

def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'name': 'Aninha',
    }) 
    
# adicionar a pasta em q está o arquivo p não haver colisões

def recipes(request, id):
    return render(request, 'recipes/pages/home.html', context={
        'name': 'Aninhaaaa',
    }) 

