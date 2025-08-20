import debug_toolbar
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='add-snippet-page'),
    path('snippets/list', views.snippets_page, {'my_snippets':False}, name='snippets-page'),
    path('snippet/<int:id>', views.snippet_detail, name='snippet-detail'),
    path('snippet/<int:id>/delete', views.snippet_delete, name="snippet-delete"),
    path('snippet/<int:id>/edit', views.snippet_edit, name="snippet-edit"),
    path('login', views.login, name="login"),
    path('logout', views.user_logout, name='logout'),
    path('snippets/my', views.snippets_page, {'my_snippets':True}, name='my-snippets'),
    path('registration', views.user_registration, name='registration'),
    path('comment/add', views.comment_add, name="comment_add"),
    path('snippets/stats', views.snippet_stats, name="snippet-stats"),
    path('notifications/', views.user_notifications, name="notifications"),
    path('profile/', views.user_profile, name="profile"),
    path('profile/edit/', views.edit_profile, name="edit-profile"),
    path('password/change/', views.password_change, name="password_change"),
    path('activate/<int:user_id>/<str:token>/', views.activate_account, name="password_change"),
    path('api/simple-data/', views.simple_api_view, name='simple_api'),
    #path('api-page/', views.api_test_page, name='api-test-page'),
    path('api/notifications/unread-count/', views.unread_notifications_count, name='unread_notifications_count'),
    path('comment/<int:id>/liked', views.comment_like,{'vote': 1}, name='comment-like'),
    path('comment/<int:id>/disliked', views.comment_like,{'vote': -1}, name='comment-dislike'),
]+ debug_toolbar_urls()

#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #urlpatterns += path('__debug__/', include(debug_toolbar.urls))
