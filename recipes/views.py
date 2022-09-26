from django.shortcuts import render
# lê e renderiza o arquivo (deixa aparecer no código fonte o HTML, etc)
from utils.recipes.factory import make_recipe

# Create your views here.

def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'recipes': [make_recipe() for _ in range(10)],
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,
    })
