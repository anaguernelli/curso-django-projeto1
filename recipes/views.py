from django.shortcuts import render
# lê e renderiza o arquivo (deixa aparecer no código fonte o HTML, etc)
from utils.recipes.factory import make_recipe
from .models import Recipe

# Create your views here.

def home(request):
    recipes = Recipe.objects.all().order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })

def category(request, category_id):
    recipes = Recipe.objects.filter(category__id=category_id).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,
    })
