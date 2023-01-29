from django.views.generic import ListView, DetailView
from django.forms.models import model_to_dict
from utils.pagination import make_pagination
from django.http import JsonResponse
from django.http import Http404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Q
from .models import Recipe
import os

PER_PAGE = int(os.environ.get('PER_PAGE', 6))
# caso não ache nada no per_page, o padrão vai ser 6
# int() para qunado fizer upload diferente, para algum servidor diferente
# não dar erro


# Class Based Views

class RecipeListViewBase(ListView):
    model = Recipe
    # paginação pronta
    paginate_by = None
    # Obj que vai por padrao pra dentro do context
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            is_published=True
        )
        # Vai uma vez na base de dados e pegando
        # esses dados e trazendo tudo de uma vez
        # O que deixa o sistema mais rápidp e gasta
        # Muito menos com servidor
        query_set = query_set.select_related(
            'author', 'category'
        )

        return query_set

    def get_context_data(self, *args, **kwargs):
        # Esse context vem de context_object_name
        context = super().get_context_data(*args, **kwargs)

        page_obj, pagination_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGE
        )

        context.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )

        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': f'{context.get("recipes")[0].category.name} - Category |'
        })

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            category__id=self.kwargs.get('category_id'),
        )

        if not query_set:
            raise Http404()

        return query_set


class RecipeDetail(DetailView):
    model = Recipe
    # não precisamos de "recipe": recipe, pois já damos
    # o nome no context_obj_name
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update(
            {'is_detail_page': True}
        )

        return ctx

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            is_published=True
        )

        return query_set


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            ),
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        context.update(
            {
                'page_title': f'Search for "{search_term}"',
                'search_term': search_term,
                'additional_url_query': f'&q={search_term}'
            }
        )

        return context


# Function Based Views

# def home(request):
#     recipes = Recipe.objects.filter(
#      is_published=True
#     ).order_by('-id')

#     page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

#     return render(request, 'recipes/pages/home.html', context={
#         'recipes': page_obj,
#         'pagination_range': pagination_range
#     })


# def category(request, category_id):
#     recipes = get_list_or_404(
#         Recipe.objects.filter(
#             category__id=category_id,
#             is_published=True,
#         ).order_by('-id')
#     )

#     page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

#     return render(request, 'recipes/pages/category.html', context={
#         'recipes': page_obj,
#        'pagination_range': pagination_range,
#        'title': f'{recipes[0].category.name} - Category |'})

# def recipe(request, id):
#     recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

#     return render(request, 'recipes/pages/recipe-view.html', context={
#         'recipe': recipe,
#         'is_detail_page': True,
#     })

# def search(request):
#     search_term = request.GET.get('q', '').strip()

#     if not search_term:
#         raise Http404()

#     recipes = Recipe.objects.filter(
#         Q(
#             Q(title__icontains=search_term) |
#             Q(description__icontains=search_term),
#         ),
#         is_published=True,
#     ).order_by('-id')

#     page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

#     return render(request, 'recipes/pages/search.html', {
#         'page_title': f'Search for "{search_term}"',
#         'search_term': search_term,
#         'recipes': page_obj,
#         'pagination_range': pagination_range,
#         'additional_url_query': f'&q={search_term}'
#     })


def theory(request, *args, **kwargs):
    # O django só chama quando é feita uma consulta
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains='Ta',
                id__gt=10,
                is_published=True) |
            Q(
                id__gt=1000
            )
        )
    )[:20]

    # try:
    #     recipes = Recipe.objects.get(pk=39283)
    # except ObjectDoesNotExist:
    #     recipes = None

    context = {
        'recipes': recipes
    }

    return render(
        request,
        'recipes/pages/theory.html',
        context=context,
    )


# JSON Response

class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        # object_list vai dar uam query set
        recipes_list = recipes.object_list.values()

        # em vez de debugar pode printar
        # print(recipes.object_list)

        return JsonResponse(
            # só aceita em forma de lista
            list(recipes_list),
            # In order to allow non-dict objects to be serialized
            # set the safe parameter to False.
            safe=False
        )


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )
