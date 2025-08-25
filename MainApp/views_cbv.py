from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from MainApp.models import Snippet
from MainApp.forms import SnippetForm, CommentForm
from django.contrib import messages
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import redirect


class AddSnippetView(LoginRequiredMixin, CreateView):
    """Создание нового сниппета"""
    model = Snippet
    form_class = SnippetForm
    template_name = 'pages/add_snippet.html'
    success_url = reverse_lazy('snippets-page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Создание сниппета'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Success!!!")
        return super().form_valid(form)



class SnippetDetailView(LoginRequiredMixin, DetailView):
    model = Snippet
    template_name = 'pages/snippet_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        snippet = self.get_object()
        context['pagename'] = f'Сниппет: {snippet.name}'
        context['comments'] = snippet.comments.all()
        context['comment_form'] = CommentForm()
        return context

    def get_queryset(self):
        return Snippet.objects.prefetch_related('comments')


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')