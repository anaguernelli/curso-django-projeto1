from urllib import request
from django.views import View
from recipes.models import Recipe
from django.http.response import Http404
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse


class DashboardRecipe(View):
    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=request.user,
                pk=id,
            ).first()

        if not recipe:
            raise Http404()

        return recipe

    def render_recipe(self, form):
        return render(
            request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form,
            }
        )

    # ao invés de dar param request e id, pode usar kwargs.get('id)
    def get(self, request, id=None):
        recipe = self.get_recipe('id')

        form = AuthorRecipeForm(
            instance=recipe
        )

        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user

            recipe.preparation_steps_is_html = False

            recipe.is_published = False
            recipe.save()

            messages.success(request, 'Your recipe has been saved!')
            return redirect(
                reverse('authors:dashboard_recipe_edit', args=(
                    recipe.id,))
            )

        return self.render_recipe(form)
