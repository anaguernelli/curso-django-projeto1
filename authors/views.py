from django.shortcuts import redirect, render

from django.http import Http404

from .forms import RegisterForm


def register_view(request):
    # exibe o formulário
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    # form que já tem dados, se tiver erros vai exibir, 
    # se tiver validado vai validar etc
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })


def register_create(request):
    # trata os dados do formulário
    if not request.POST:
        raise Http404()
        # se o método que vir no create não for POST, for GET
        # vai levantar um erro

    POST = request.POST
    request.session['register_form_data'] = POST
    # salvando o dicionário do POST inteiro
    form = RegisterForm(POST)

    return redirect('authors:register')
    # redirecionar para a view register_view
