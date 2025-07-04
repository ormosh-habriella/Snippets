from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet, LANG_ICONS
from MainApp.forms import SnippetForm, UserRegistrationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def get_icon_class(lang):
    return LANG_ICONS.get(lang)
def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@login_required
def add_snippet_page(request):
    if request.method == 'GET':
        form = SnippetForm()
        context = {'form': form, "pagename": "Создание сниппета"}
        return render(request, 'pages/add_snippet.html', context)

    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return redirect('snippets-page')
        else:
            context = {'form': form, "pagename": "Создание сниппета"}
            return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    if request.user.is_authenticated:  # auth: all public + self private
        snippets = Snippet.objects.filter(Q(public=True) | Q(public=False, user=request.user))
    else:  # not auth: all public
        snippets = Snippet.objects.filter(public=True)
    for snippet in snippets:
        snippet.icon_class = get_icon_class(snippet.lang)
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, id):
    snippet = get_object_or_404(Snippet, id=id)
    snippet.views_count = F('views_count') + 1
    snippet.save(update_fields=['views_count'])
    snippet.refresh_from_db()
    context = {
        'pagename': f'Сниппет: {snippet.name}',
        'snippet': snippet
    }
    return render(request, 'pages/snippet_detail.html', context)


def snippet_delete(request, id):
    snippet = get_object_or_404(Snippet, id=id)
    snippet.delete()

    return redirect('snippets-page')


def snippet_edit(request, id):
    if request.method == "GET":
        snippet = get_object_or_404(Snippet, id=id)
        form = SnippetForm(instance=snippet)
        context = {
            "pagename": "Редактировать Сниппет",
            "form": form,
            "edit": True,
            "id": id
        }
        return render(request, 'pages/add_snippet.html', context)

    if request.method == "POST":
        snippet = get_object_or_404(Snippet, id=id)
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()

        return redirect('snippets-page')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            context = {
                "errors": "Неверный username или password",
            }
            return render(request, "pages/index.html", context)


def user_logout(request):
    auth.logout(request)
    return redirect('home')

@login_required()
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def user_registration(request):
   if request.method == "GET": # page with form
       form = UserRegistrationForm()
       context = {
           "form": form
       }
       return render(request, "pages/registration.html", context)

   if request.method == "POST": # form data
       form = UserRegistrationForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('home')
       else:
           context = {
               "form": form,
           }
           return render(request, "pages/registration.html", context)