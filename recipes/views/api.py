from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Recipe
from tag.models import Tag
from ..serializers import RecipeSerializer, TagSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..permissions import IsOwner
from django.shortcuts import get_object_or_404


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 1


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        # &category_id=1
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    # sobrescrevendo o método que existe no django restf
    # para garantir que quando eu buscar uma recipe qualquer,
    # sempre que utilizá-lo vai checar as object permissions
    def get_object(self):
        pk = self.kwargs.get('pk', '')

        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
            # poderia fazer dessa forma, mas estamos usando
            # as permissões do django
            # author=self.request.user
        )

        self.check_object_permissions(self.request, obj)

        return obj

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            # para patch e delete a permissão usada é esta
            return [IsOwner(), ]

        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        # self.request.user é a msm request só que dentro da class
        print('REQUEST', request.user, self.request.user)
        print(request.user.is_authenticated)
        # sem o Bearer token, o usuário fica como anônimo
        return super().list(request, *args, **kwargs)

    def parcial_update(self, request, *args, **kwargs):
        recipe = self.get_object()
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
