from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin

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
]
