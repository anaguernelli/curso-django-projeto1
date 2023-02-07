from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Recipe
from tag.models import Tag
from ..serializers import RecipeSerializer, TagSerializer
from rest_framework import status


@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    # lendo todas as recipes
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    elif request.method == 'POST':
        # criando uma recipe
        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author_id=1, category_id=1,
            tags=[1, 2]
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['get', 'patch', 'delete'])
def recipe_api_detail(request, pk):
    recipes = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )

    if request.method == 'GET':
        serializer = RecipeSerializer(
            instance=recipes,
            many=False,
            context={'request': request}
        )
        return Response(serializer.data)

    elif request.method == 'PATCH':
        # uma mistura de read e create
        serializer = RecipeSerializer(
            instance=recipes,
            data=request.data,
            many=False,
            context={'request': request},
            # deve informar que é uma atualização parcial
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,)

    elif request.method == 'DELETE':
        recipes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )

    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request}
    )

    return Response(serializer.data)
