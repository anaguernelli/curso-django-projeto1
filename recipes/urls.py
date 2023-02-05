from django.urls import path

from recipes import views
# . (dot) - path where you already is


app_name = 'recipes'

urlpatterns = [
    path(
        '',
        views.RecipeListViewHome.as_view(),
        name='home'
    ),
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(),
        name='category'
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetail.as_view(),
        name='recipe'
    ),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(),
        name='search'
    ),
    path(
        'recipes/api/v1/',
        views.RecipeListViewHomeApi.as_view(),
        name='recipe_api_v1'
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailAPI.as_view(),
        name="recipes_api_v1_detail",
    ),
    path(
        'theory/',
        views.theory,
        name="theory",
    ),
    path(
        'recipes/tags/<slug:slug>',
        views.RecipeListViewTag.as_view(),
        name="tag",
    ),
    path(
        'recipes/api/v2/',
        views.recipe_api_list,
        name='recipe_api_v2'
    ),
]

# int - Matches zero or any positive integer. Returns an int.
# slug - Matches any slug string consisting of ASCII letters or numbers, plus
# hyphen and underscore characters. For example,
# building-your-1st-django-views.
