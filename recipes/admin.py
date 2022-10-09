from django.contrib import admin
from .models import Category, Recipe

# Register your models here, pr your model won't appear in the adm area

class CategoryAdmin(admin.ModelAdmin):
    ...



@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...



admin.site.register(Category, CategoryAdmin)







