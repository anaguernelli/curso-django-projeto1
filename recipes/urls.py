from django.urls import path

from . import views

# . (dot) - path where you already is


app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path(
        'recipes/category/<int:category_id>/', 
        views.category, 
        name='category'),
    path('recipes/<int:id>/', views.recipe, name='recipe'),
]

# int - Matches zero or any positive integer. Returns an int.
# slug - Matches any slug string consisting of ASCII letters or numbers, plus
# hyphen and underscore characters. For example,
# building-your-1st-django-site.
