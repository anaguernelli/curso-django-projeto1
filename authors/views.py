from django.shortcuts import redirect, render

from django.http import Http404

from .forms import RegisterForm, LoginForm

from django.contrib import messages

from django.urls import reverse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from recipes.models import Recipe


def register_view(request):
    # exibe o formulário
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    # form que já tem dados, se tiver erros vai exibi-los,
    # se tiver validado vai validar etc
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    # trata os dados do formulário
    if not request.POST:
        raise Http404()
        # se o método que vir no create não for POST,
        # vai levantar um erro

    POST = request.POST
    request.session['register_form_data'] = POST
    # salvando o dicionário do POST inteiro
    form = RegisterForm(POST)
    # quer salvar os dados do formulário na sessão (django session)

    if form.is_valid():
        user = form.save(commit=False)
        # não iremos salvar a password (na forma de string)
        # iremos tratá-la primeiro
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')

        del(request.session['register_form_data'])
        # depois q cadastrado, é direcionado para url de login
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    # exibição do form
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    # tratando os dados do formulário usando authenticate e login
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')

    # se não for válida
    else:
        messages.error(request, 'Invalid username or password')

    # redireciona para a page de login
    return redirect(login_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))

    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        # as receitas nao devem estar publicadas
        # e o autor deve ser a pessoal q está atualmente logada
        is_published=False,
        author=request.user
    )
    return render(
        request,
        'authors/pages/dashboard.html',
        context={
            'recipes': recipes,
        }
    )

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    )

    if not recipe:
        raise Http404()
    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
        }
    )