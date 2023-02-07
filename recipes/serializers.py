# converte um model para um formato que seja entendível como JSON
from rest_framework import serializers
from tag.models import Tag
from .models import Recipe
from authors.validators import AuthorRecipeValidator


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
            'tag_links', 'preparation_time',
            'preparation_time_unit', 'servings', 'servings_unit',
            'preparation_steps', 'cover'
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
        # dados iniciais que vêm no form
        # self.initial_data

        # dados já salvos/dados que você receb do seu cliente
        # self.data

        # dados depois de validar
        # self.validated_data

        # porém, já estamos recebendo os dados de attrs
        AuthorRecipeValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError
        )
        # Aqui, só podemos receber o ValidationError com o serializer

        return super().validate(attrs)
