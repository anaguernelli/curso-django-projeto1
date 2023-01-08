from django.shortcuts import redirect, render

from django.http import Http404

from .forms import RegisterForm

from django.contrib import messages


def register_view(request):
    # exibe o formulário
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    # form que já tem dados, se tiver erros vai exibi-los,
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
    # quer salvar os dados do formulário na sessão (session )

    if form.is_valid():
        form.save()
        messages.success(request, 'Your user is created, please log in.')

        del(request.session['register_form_data'])

    return redirect('authors:register')
