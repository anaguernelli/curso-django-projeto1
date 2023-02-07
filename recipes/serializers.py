# converte um model para um formato que seja entendível como JSON
from collections import defaultdict
from rest_framework import serializers
from tag.models import Tag
from .models import Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        # SEMPRE coloque todos os fields manualmente!!!
        fields = [
            'author', 'id', 'title', 'description', 'category',
            'tags', 'public', 'preparation', 'tag_objects',
            'tag_links'
        ]
    # os campos que estão personalizados, deve manter
    public = serializers.BooleanField(
        source='is_published',
        # não se esqueça de dizer s eo campo é só de leitura
        read_only=True,
    )
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name',
        read_only=True,
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )
    tag_objects = TagSerializer(
        many=True,
        source='tags',
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True,
    )

    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        # usamos validate quando precisamos do valor de mais
        # de um campo para fazer validação
        _my_errors = defaultdict(list)

        title = attrs.get('title')
        description = attrs.get('description')

        if title == description:
            raise serializers.ValidationError(
                {
                    "title": ["alo", "posso", "ter mais", "de um erro"],
                    "description": ["alo", "posso", "ter mais", "de um erro"]
                }
            )

        return super().validate(attrs)

    def validate_title(self, value):
        # validate_field quando o valor de um campo já serve para a validação
        title = value

        if len(title) < 5:
            raise serializers.ValidationError('Must have at least 5 chars.')

        return title
