from django.urls import path

from . import views 
# the command above is to not put views in sequence
# . (dot) - path where you already is

urlpatterns = [
    path('', views.home),
    path('recipes/<int:id>/', views.recipe),
]

# int - Matches zero or any positive integer. Returns an int.
# slug - Matches any slug string consisting of ASCII letters or numbers, plus the hyphen and underscore characters. For example, building-your-1st-django-site.