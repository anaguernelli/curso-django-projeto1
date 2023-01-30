from django.contrib import admin
from .models import Tag


# Registrando o app Tag na Admin
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # campos exibidos
    list_display = 'id', 'name', 'slug',
    # campos que vão ter links
    list_display_links = 'id', 'slug'
    # campos de busca
    search_fields = 'id', 'slug', 'name',
    list_per_page = 10
    list_editable = 'name',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('name',),
    }
