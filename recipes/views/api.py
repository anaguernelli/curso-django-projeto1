from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Recipe
from tag.models import Tag
from ..serializers import RecipeSerializer, TagSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 1


class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination

    # def get(self, request):
    #     recipes = Recipe.objects.get_published()[:10]
    #     serializer = RecipeSerializer(
    #         instance=recipes,
    #         many=True,
    #         context={'request': request}
    #     )

    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = RecipeSerializer(
    #         data=request.data,
    #         context={'request': request}
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_201_CREATED
    #     )


class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination

    # Estamos sobrescrevendo o método partial_update
    def patch (self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        recipe = self.get_queryset().filter(pk=pk).first()
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data
        )

    # def get_recipe(self, pk):
    #     recipe = get_object_or_404(
    #         Recipe.objects.get_published(),
    #         pk=pk
    #     )

    #     return recipe

    # def get(self, request, pk):
    #     serializer = RecipeSerializer(
    #         instance=self.get_recipe(pk),
    #         many=False,
    #         context={"request": request}
    #     )

    #     return Response(serializer.data)

    # def patch(self, request, pk):
    #     serializer = RecipeSerializer(
    #         instance=self.get_recipe(pk),
    #         data=request.data,
    #         many=False,
    #         partial=True,
    #         context={"request": request}
    #     )

    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data)

    # def delete(self, request, pk):
    #     recipe = self.get_recipe(pk)
    #     recipe.delete()

    #     return Response(status=status.HTTP_204_NO_CONTENT)


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
