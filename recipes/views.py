from django.http import Http404

from django.db.models import Q

from utils.pagination import make_pagination
# lê e renderiza o arquivo (deixa aparecer no código fonte o HTML, etc)
from .models import Recipe

from django.views.generic import ListView, DetailView

import os

PER_PAGE = int(os.environ.get('PER_PAGE', 6))
# caso não ache nada no per_page, o padrão vai ser 6
# int() para qunado fizer upload diferente, para algum servidor diferente
# não dar erro


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


# def home(request):
#     recipes = Recipe.objects.filter(
#      is_published=True
#     ).order_by('-id')

#     page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

#     return render(request, 'recipes/pages/home.html', context={
#         'recipes': page_obj,
#         'pagination_range': pagination_range
#     })


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

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            is_published=True
        )

        return query_set


# def recipe(request, id):
#     recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

#     return render(request, 'recipes/pages/recipe-view.html', context={
#         'recipe': recipe,
#         'is_detail_page': True,
#     })


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
