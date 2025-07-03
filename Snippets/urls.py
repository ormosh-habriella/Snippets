from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='add-snippet-page'),
    path('snippets/list', views.snippets_page, name='snippets-page'),
    path('snippet/<int:id>', views.snippet_detail, name='snippet-detail'),
    path('snippet/<int:id>/delete', views.snippet_delete, name="snippet-delete"),
    path('snippet/<int:id>/edit', views.snippet_edit, name="snippet-edit"),
    path('login', views.login, name="login"),
    path('logout', views.user_logout, name='logout'),
    path('snippets/my', views.my_snippets, name='my-snippets'),
    path('registration', views.user_registration, name='registration'),
]
