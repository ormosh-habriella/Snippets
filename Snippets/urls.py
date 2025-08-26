
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views, views_cbv
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index_page, name='home'),
    #path('snippets/add', views.add_snippet_page, name='add-snippet-page'),
    path('snippets/add', views_cbv.AddSnippetView.as_view(), name='add-snippet-page'),
    path('snippets/list', views.snippets_page, {'my_snippets':False}, name='snippets-page'),
    #path('snippet/<int:id>', views.snippet_detail, name='snippet-detail'),
    path('snippet/<int:pk>', views_cbv.SnippetDetailView.as_view(), name='snippet-detail'),
    path('snippet/<int:id>/delete', views.snippet_delete, name="snippet-delete"),
    path('snippet/<int:id>/edit', views.snippet_edit, name="snippet-edit"),
    path('login', views.login, name="login"),
    #path('logout', views.user_logout, name='logout'),
    path('logout', views_cbv.UserLogoutView.as_view(), name='logout'),
    path('snippets/my', views.snippets_page, {'my_snippets':True}, name='my-snippets'),
    path('registration', views.user_registration, name='registration'),
    path('comment/add', views.comment_add, name="comment_add"),
    path('snippets/stats', views.snippet_stats, name="snippet-stats"),
    path('notifications/', views.user_notifications, name="notifications"),
    path('profile/', views.user_profile, name="profile"),
    path('profile/edit/', views.edit_profile, name="edit-profile"),
    path('password/change/', views.password_change, name="password_change"),
    path('snippet/subscribe/', views.snippet_subscribe, name="snippet-subscribe"),
    path('snippet/unsubscribe/', views.snippet_unsubscribe, name="snippet-unsubscribe"),
    path('subscriptions/', views.my_subscriptions, name='my-subscriptions'),
    path('activate/<int:user_id>/<str:token>/', views.activate_account, name="activate-account"),
    path('resend_email/', views.resend_email, name="resend-email"),
    path('api/simple-data/', views.simple_api_view, name='simple_api'),
    #path('api-page/', views.api_test_page, name='api-test-page'),
    path('api/notifications/unread-count/', views.unread_notifications_count, name='unread_notifications_count'),
    path('comment/<int:id>/liked', views.comment_like,{'vote': 1}, name='comment-like'),
    path('comment/<int:id>/disliked', views.comment_like,{'vote': -1}, name='comment-dislike'),
]
# Добавляем debug_toolbar URLs только в режиме разработки
if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass

# Добавляем обработку статических файлов только в режиме разработки
# В продакшене Django использует встроенную обработку статических файлов
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
