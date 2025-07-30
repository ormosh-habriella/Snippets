import pytest
from .views import index_page, add_snippet_page, snippets_page, snippet_detail
from django.urls import reverse
from django.test import Client
from django.test import RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from .models import Snippet

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware


def add_messages_and_session_to_request(request):
    # Attach session for messages to work correctly
    middleware = SessionMiddleware(lambda r: None)  # Mock the get_response callable
    middleware.process_request(request)
    request.session.save()  # Ensure a session key is generated

    # Attach message storage
    setattr(request, '_messages', FallbackStorage(request))


class TestIndexPage:
    def test_index(self):
        client = Client()
        response = client.get(reverse('home'))

        assert response.status_code == 200
        assert 'Добро пожаловать' in response.content.decode()
        assert response.context.get('pagename') == 'PythonBin'


@pytest.mark.django_db
class TestAddSnippetPage:
    def setup_method(self):
        self.factory = RequestFactory()

    def test_gest_user(self):
        request = self.factory.get(reverse('add-snippet-page'))
        request.user = AnonymousUser()
        response = add_snippet_page(request)

        assert response.status_code == 302

    def test_auth_user(self):
        request = self.factory.get(reverse('add-snippet-page'))
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        request.user = user
        response = add_snippet_page(request)

        assert response.status_code == 200

    def test_post_form_data(self):
        form_data = {
            "name": "Test form snippet",
            "lang": "python",
            "code": "simple py code",
            "public": True,
        }
        user = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpass123"
        )
        request = self.factory.post(reverse('add-snippet-page'), form_data)
        request.user = user
        add_messages_and_session_to_request(request)
        response = add_snippet_page(request)

        snippet = Snippet.objects.get(id=1)

        assert response.status_code == 302
        assert snippet.name == form_data["name"]
        assert snippet.lang == form_data["lang"]
        assert snippet.public == form_data["public"]


@pytest.mark.django_db
class TestSnippetDelete:
    def setup_method(self):
        self.client = Client()

    def test_gest_user(self):
        response = self.client.get(reverse('snippet-delete', kwargs={'id': '2'}))

        assert response.status_code == 404

    def test_delete_not_existing(self):
        response = self.client.get(reverse('snippet-delete', kwargs={'id': '2'}))

        assert response.status_code == 404


    def test_delete(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

        Snippet.objects.create(
            name = 'For delete',
            lang = 'python',
            code = 'snippet code',
            user = user
        )
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('snippet-delete', kwargs={'id': 1}))

        assert response.status_code == 302
        assert Snippet.objects.count() == 0