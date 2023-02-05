from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def recipe_api_list(request):
    # request são dados do cliente e temos
    # que retornar uma resposta
    return Response('ok')
