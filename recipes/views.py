from django.views.generic import ListView, DetailView
from django.forms.models import model_to_dict
from utils.pagination import make_pagination
from django.http import JsonResponse
from django.http import Http404
from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import render
from .models import Recipe
from tag.models import Tag
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

        query_set = query_set.select_related(
            'author', 'category'
        )
        # uma busca na foreign key do author
        # nao botamos select pq não é uma fk q pode ser seguida
        # diretamente pelo django, E se houver uma consulta com 6+ outer joins,
        # é preferível então que troque o select pelo prefetch related
        query_set = query_set.prefetch_related('tags', 'author__profile')

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


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            # tags__slug é basicamente o campo tags no models que faz
            # uma genericRelation com com Tag e a Tag tem o campo slug
            tags__slug=self.kwargs.get('slug', '')
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag'

        context.update(
            {
                'page_title': page_title,
            }
        )

        return context

# Function Based Views


def theory(request, *args, **kwargs):
    recipes = Recipe.objects.get_published()

    number_of_recipes = recipes.aggregate(number=Count('id'))

    context = {
        'recipes': recipes,
        # Retorna um dicionário
        'number_of_recipes': number_of_recipes['number'],
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
