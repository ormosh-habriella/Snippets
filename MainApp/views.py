from django.db.models import F, Q, Count, Avg
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet, LANG_ICONS, Comment, LANG_CHOICES
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages
from MainApp.signals import snippet_view


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
            messages.success(request, 'Сниппет успешно создан')
            return redirect('snippets-page')
        else:
            if form.errors.get('name'):
                messages.error(request, f'Название должно содержать не менее 3 но не больше 20 символов')
            context = {'form': form, "pagename": "Создание сниппета"}
            return render(request, 'pages/add_snippet.html', context)


def snippets_page(request, my_snippets):
    if my_snippets:
        if not request.user.is_authenticated:
            raise PermissionDenied
        pagename = 'Мои сниппеты'
        snippets = Snippet.objects.filter(user=request.user)
    else:
        pagename = 'Просмотр сниппетов'
        if request.user.is_authenticated:  # auth: all public + self private
            snippets = Snippet.objects.filter(Q(public=True) | Q(public=False, user=request.user))
        else:  # not auth: all public
            snippets = Snippet.objects.filter(public=True)

        # search
    search = request.GET.get("search")
    if search:
        snippets = snippets.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search) |
            Q(description__icontains=search)
        )

        # filter
    lang = request.GET.get("lang")
    if lang:
        snippets = snippets.filter(lang=lang)

    user_id = request.GET.get("user_id")
    if user_id:
        snippets = snippets.filter(user__id=user_id)

        # sort
    sort = request.GET.get("sort")
    if sort:
        snippets = snippets.order_by(sort)



    # TODO: работает или пагинация или сортировка по полю!
    paginator = Paginator(snippets, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # users = User.objects.filter(snippet__isnull=False).distinct()
    #
    # snippets_count = Snippet.objects.count()

    users = User.objects.annotate(
        snippet_count=Count('snippet', filter=Q(snippet__public=True))
    ).filter(snippet_count__gt=0)

    context = {
        'pagename': pagename,
        'snippets': snippets,
        'sort': sort,
        'page_obj': page_obj,
        'LANG_CHOICES': LANG_CHOICES,
        'users': users,
        'lang': lang,
        'user_id': user_id,
        'request': request,
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, id):
    # snippet = get_object_or_404(Snippet, id=id)
    snippet = Snippet.objects.prefetch_related("comments").get(id=id)
    # Отправляем сигнал
    snippet_view.send(sender=None, snippet=snippet)
    comments = Comment.objects.all()
    comment_form = CommentForm()
    context = {
        'pagename': f'Сниппет: {snippet.name}',
        'snippet': snippet,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'pages/snippet_detail.html', context)


def snippet_delete(request, id):
    snippet = get_object_or_404(Snippet, id=id)
    if snippet.user != request.user:
        raise PermissionDenied()
    snippet.delete()
    messages.success(request, 'Сниппет был успешно удален')

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
            messages.success(request, 'Сниппет был успешно отредактирован')

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


# @login_required()
# def my_snippets(request):
#     snippets = Snippet.objects.filter(user=request.user)
#     paginator = Paginator(snippets, 2)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'pagename': 'Мои сниппеты',
#         'snippets': snippets,
#         'page_obj': page_obj,
#     }
#     return render(request, 'pages/view_snippets.html', context)


def user_registration(request):
    if request.method == "GET":  # page with form
        form = UserRegistrationForm()
        context = {
            "form": form
        }
        return render(request, "pages/registration.html", context)

    if request.method == "POST":  # form data
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # --- ОТПРАВКА СООБЩЕНИЯ ---
            messages.success(request, f'Добро пожаловать, {user.username}! Вы успешно зарегистрированы.')
            # --- КОНЕЦ ОТПРАВКИ СООБЩЕНИЯ ---
            return redirect('home')
        else:
            context = {
                "form": form,
            }
            return render(request, "pages/registration.html", context)


@login_required()
def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snippet_id = request.POST.get('snippet_id')  # Получаем ID сниппета из формы
        snippet = get_object_or_404(Snippet, id=snippet_id)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user  # Текущий авторизованный пользователь
            comment.snippet = snippet
            comment.save()
            messages.success(request, 'Комментарий был успешно добавлен')

        return redirect('snippet-detail',
                        id=snippet_id)  # Предполагаем, что у вас есть URL для деталей сниппета с параметром pk

    raise Http404


def snippet_stats(request):
    snippets = Snippet.objects.aggregate(snippets_count=Count('id'),
                                         public_snippets_count=Count('id', filter=Q(public=True)),
                                         average_views_count=Avg('views_count'))
    top5_snippets = Snippet.objects.order_by("-views_count").values("name", "views_count")[:5]
    top3_users = User.objects.annotate(snippets_count=Count('snippet')).order_by("-snippets_count").values("username", "snippets_count")[:3]

    context = {
        'snippets': snippets,
        'top5_snippets': top5_snippets,
        'top3_users': top3_users,
        'pagename': 'Статистика по сниппетам',
    }

    return render(request, "pages/snippet_stats.html", context)
