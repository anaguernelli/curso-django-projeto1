from django.urls import path

from . import views 
# utiliza o comando de cima em vez de pôr sequenciado
# . (ponto) - da pasta em que já está

urlpatterns = [
    path('', views.home),
    path('recipes/<int:id>/', views.recipes),
]

# int - Matches zero or any positive integer. Returns an int.
# slug - Matches any slug string consisting of ASCII letters or numbers, plus the hyphen and underscore characters. For example, building-your-1st-django-site.