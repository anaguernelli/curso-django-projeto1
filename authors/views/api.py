from rest_framework.viewsets import ReadOnlyModelViewSet
from ..serializers import AuthorSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


# User será permitido somente a ler
class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(
            # não permite q um user veja dados de outros usuários
            # apenas o dele mesmo
            username=self.request.user.username
        )
        return qs

    @action(
            methods=['get'],
            detail=False,
    )
    # criando uma url com dados de perfil utilizando o DRF
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(instance=obj)

        return Response(serializer.data)
