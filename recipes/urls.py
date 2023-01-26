from django.urls import path

from . import views

# . (dot) - path where you already is


app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(),
        name='category'),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(),
        name='search'),

]

# int - Matches zero or any positive integer. Returns an int.
# slug - Matches any slug string consisting of ASCII letters or numbers, plus
# hyphen and underscore characters. For example,
# building-your-1st-django-site.
