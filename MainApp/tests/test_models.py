from django.db import transaction
from django.test import TestCase
import pytest
from MainApp.models import Snippet, Tag, Comment
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestSnippetModel:
    def test_create_snippet(self):
        snippet = Snippet.objects.create(
            name="Test Snippet",
            lang="python",
            code="print('Hello World!')",
            public=True,
        )

        snippet = Snippet.objects.get(id=1)

        assert snippet.name == "Test Snippet"
        assert snippet.lang == "python"
        assert snippet.views_count == 0
        assert snippet.public


    def test_user_create_snippet(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

        snippet = Snippet.objects.create(
            name="User Snippet",
            lang="javascript",
            code="console.log('Hello');",
            user=user,
            public=False
        )

        assert snippet.user.username == "testuser"
        assert not snippet.public
        assert snippet.code == "console.log('Hello');"

@pytest.mark.django_db
class TestTagModel:
        """Тесты для модели Tag"""

        def test_tag_creation(self):
            """Тест создания тега"""
            tag = Tag.objects.create(name="Python")
            assert tag.name == "Python"

        def test_duplicate_tag_names_not_allowed(self):
            """Тест, что теги с одинаковыми именами недопустимы"""
            from django.db import IntegrityError

            # Создаем первый тег
            tag1 = Tag.objects.create(name="Python")

            # Пытаемся создать второй тег с тем же именем
            # Должно возникнуть исключение IntegrityError
            with pytest.raises(IntegrityError):
                with transaction.atomic():
                    Tag.objects.create(name="Python")

            # Проверяем, что в базе данных остался только один тег с именем "Python"
            assert Tag.objects.filter(name="Python").count() == 1
            assert Tag.objects.get(name="Python") == tag1


@pytest.mark.django_db
class TestCommentModel:
    """Тесты для модели Comment"""

    def test_comment_creation(self):
        """Тест создания комментария"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

        snippet = Snippet.objects.create(
            name="User Snippet",
            lang="javascript",
            code="console.log('Hello');",
            user=user,
            public=False
        )


        comment = Comment.objects.create(
            text = "good code",
            author = user,
            snippet = snippet,
        )

        assert comment.text == "good code"


