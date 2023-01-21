from django.contrib import admin
from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # Todos esses lists, você encontra na documentação do django
    # Deve declarar primeiro no list_display para distribuir para outras list
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    # vai tornar os atributos dados em links
    list_display_links = 'title', 'created_at',
    # Sistema de busca
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps',
    # Filtro
    list_filter = 'category', 'author', 'is_published', \
        'preparation_steps_is_html',
    list_per_page = 10
    # o is_published pode ser editado
    list_editable = 'is_published',
    ordering = '-id',
    # Vai criar uma slug automaticamente com o titulo nesse caso
    prepopulated_fields = {
        "slug": ('title',)
    }


admin.site.register(Category, CategoryAdmin)
