from django.urls import path, include

from recipes import views
from rest_framework.routers import SimpleRouter

app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(
    'recipes/api/v2',
    views.RecipeAPIv2ViewSet,
    # Se não tiver uma queryset definida no Viewset,
    # é obrigado declarar um basename
    basename='recipes-api'
    # no router, o path estará como recipes-api-list/recipe-api-detail
    # entenda por list = create, detail = retrieve, partial_update, destroy
)

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
    # path(
    #     'recipes/api/v2/',
    #     views.RecipeAPIv2ViewSet.as_view({
    #         'get': 'list',
    #         'post': 'create',
    #     }),
    #     name='recipes_api_v2',
    # ),
    # path(
    #     'recipes/api/v2/<int:pk>/',
    #     views.RecipeAPIv2ViewSet.as_view({
    #         'get': 'retrieve',
    #         'patch': 'partial_update',
    #         'delete': 'destroy'
    #     }),
    #     name='recipes_api_v2_detail',
    # ),
    path(
        'recipes/api/v2/tag/<int:pk>/',
        views.tag_api_detail,
        name='recipes_api_v2_tag',
    ),
    # outra forma de incluir nosso simplerouter com include
    path('',  include(recipe_api_v2_router.urls)),
]

# estamos concatenando com urlpatterns

# urlpatterns += recipe_api_v2_router.urls
