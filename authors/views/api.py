from rest_framework.viewsets import ReadOnlyModelViewSet
from ..serializers import AuthorSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated


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
