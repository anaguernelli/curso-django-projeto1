from django.urls import path
from . import views


app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register',),
    path('register/create/', views.register_create, name='register_create',),
    path('login/', views.login_view, name='login',),
    path('login/create/', views.login_create, name='login_create',),
    path('logout/', views.logout_view, name='logout',),
    path('dashboard/', views.dashboard, name='dashboard',),
    path(
        'dashboard/recipe/create/',
        views.dashboard_recipe_create,
        name='dashboard_recipe_create',
    ),
    path(
        'dashboard/recipe/delete/',
        views.dashboard_recipe_delete,
        name='dashboard_recipe_delete',
    ),
    path(
        'dashboard/recipe/<int:id>/edit/',
        views.DashboardRecipe.as_view(),
        name='dashboard_recipe_edit',
    ),

]
