from django.db import IntegrityError
from django.db.models import F, Q, Count, Avg
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet, LANG_ICONS, Comment, LANG_CHOICES, Notification, LikeDislike, SnippetSubscription
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import messages
from MainApp.signals import snippet_view
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from MainApp.utils import verify_activation_token, send_activation_email


def index_page(request):
    context = {'pagename': 'PythonBin'}
    messages.success(request, 'Добро пожаловать на сайт')
    messages.warning(request, 'Доработать закрытие сообщений по таймеру')
    messages.warning(request, 'Доработать закрытие сообщений по таймеру')
    messages.warning(request, 'Доработать закрытие сообщений по таймеру')
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


def snippets_page(request, my_snippets, num_snippets_on_page=5):
    if my_snippets:
        if not request.user.is_authenticated:
            raise PermissionDenied
        pagename = 'Мои сниппеты'
        snippets = Snippet.objects.filter(user=request.user)
    else:
        pagename = 'Просмотр сниппетов'
        if request.user.is_authenticated:  # auth: all public + self private
            snippets = Snippet.objects.filter(Q(public=True) | Q(public=False, user=request.user)).select_related("user")
        else:  # not auth: all public
            snippets = Snippet.objects.filter(public=True).select_related("user")

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
    paginator = Paginator(snippets, num_snippets_on_page)
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
            if user.is_active:
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
            send_activation_email(user, request)
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


@login_required
def user_notifications(request):
    """Страница с уведомлениями пользователя"""
    # Отмечаем все уведомления как прочитанные при переходе на страницу
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)

    # Получаем все уведомления для авторизованного пользователя, сортируем по дате создания
    notifications = Notification.objects.filter(recipient=request.user)

    context = {
        'pagename': 'Мои уведомления',
        'notifications': notifications
    }
    return render(request, 'pages/notifications.html', context)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def simple_api_view(request):
    """
    Простой API endpoint для обработки GET и POST запросов
    """

    if request.method == 'GET':
        # Обработка GET запроса
        try:
            # Здесь может быть логика получения данных из базы
            data = {
                'success': True,
                'message': 'Данные успешно получены!',
                'timestamp': str(datetime.now()),
                'items': [
                    {'id': 1, 'name': 'Элемент 1'},
                    {'id': 2, 'name': 'Элемент 2'},
                    {'id': 3, 'name': 'Элемент 3'}
                ]
            }
            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    elif request.method == 'POST':
        # Обработка POST запроса
        try:
            # Парсим JSON данные из запроса
            data = json.loads(request.body)

            # Обрабатываем полученные данные
            received_message = data.get('message', '')

            # Здесь может быть логика сохранения в базу данных

            response_data = {
                'success': True,
                'message': f'Получено сообщение: {received_message}',
                'processed': True
            }

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Неверный формат JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@login_required
def unread_notifications_count(request):
    """
    API endpoint для получения количества непрочитанных уведомлений
    Использует long polling - отвечает только если есть непрочитанные уведомления
    """
    import time

    # Максимальное время ожидания (30 секунд)
    max_wait_time = 10
    check_interval = 1  # Проверяем каждую секунду

    last_count = int(request.GET.get("last_count", 0))

    start_time = time.time()
    unread_count = 0

    while time.time() - start_time < max_wait_time:
        # Получаем количество непрочитанных уведомлений
        unread_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()

        # Если есть непрочитанные уведомления, сразу отвечаем
        if unread_count > last_count:
            return JsonResponse({
                'success': True,
                'unread_count': unread_count,
                'timestamp': str(datetime.now())
            })

        # Ждем перед следующей проверкой
        time.sleep(check_interval)

    # Если время истекло и нет уведомлений, возвращаем 0
    return JsonResponse({
        'success': True,
        'unread_count': unread_count,
        'timestamp': str(datetime.now())
    })


@login_required
def comment_like(request, id, vote):
    comment = get_object_or_404(Comment, id=id)
    user = request.user

    try:
        LikeDislike.objects.create(
            user=user,
            content_object=comment,
            vote=vote
        )
    except IntegrityError:
        like = LikeDislike.objects.get(user=user, object_id=id)
        like.delete()

    LikeDislike.objects.create(
        user=user,
        content_object=comment,
        vote=vote
    )

    return redirect('snippet-detail', id=comment.snippet.id)


def user_profile(request):
    user = request.user
    snippets = Snippet.objects.filter(user=user)

    all_snippets = snippets.count()
    avg_views = snippets.aggregate(Avg('views_count'))['views_count__avg']
    top_snippets = snippets.order_by('-views_count')[:5]

    snippet_actions = [
        {'description': f'Создан сниппет "{s.name}"', 'date': s.creation_date, 'type': 'snippet_created'}
        for s in snippets
    ]
    comments = Comment.objects.filter(author=user)
    comment_actions = [
        {'description': f'Добавлен комментарий к "{c.snippet.name}"', 'date': c.creation_date, 'type': 'comment_added'}
        for c in comments
    ]
    user_actions = sorted(snippet_actions + comment_actions, key=lambda x: x['date'], reverse=True)[:20]

    context = {
        'profile_user': user,
        'all_snippets': all_snippets,
        'avg_views': avg_views,
        'top_snippets': top_snippets,
        'user_actions': user_actions,
    }
    return render(request, 'pages/user_profile.html', context)


def edit_profile(request):
    ...


def password_change(request):
    ...


def activate_account(request, user_id, token):
    """
    Подтверждение аккаунта пользователя по токену
    """
    try:
        user = User.objects.get(id=user_id)

        # Проверяем, не подтвержден ли уже аккаунт
        if user.is_active:
            messages.info(request, 'Ваш аккаунт уже подтвержден.')
            return redirect('home')

        # Проверяем токен
        if verify_activation_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request,
                             'Ваш аккаунт успешно подтвержден! Теперь вы можете войти в систему.')
            return redirect('home')
        else:
            messages.error(request,
                           'Недействительная ссылка для подтверждения. Возможно, она устарела.')
            return redirect('home')

    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден.')
        return redirect('home')


@login_required
def snippet_subscribe(request):
    if request.method == 'POST':
        snippet_id = request.POST.get('id')
        snippet = get_object_or_404(Snippet, id=snippet_id)
        SnippetSubscription.objects.get_or_create(user=request.user, snippet=snippet)

        return redirect('snippet-detail', pk=snippet_id)