import pytest
from MainApp.models import Tag, Snippet, Comment
from MainApp.factories import TagFactory, SnippetFactory, CommentFactory


@pytest.mark.django_db
def test_create_tags(tag_factory):
    # Создаст три тега, с указанными именами
    tags = tag_factory(names=["js", "basic", "oop"])

    assert Tag.objects.count() == 3



@pytest.fixture
def snippet():
    return SnippetFactory()


@pytest.fixture
def comment_factory():
    def create_comment_to_snippet(snippet, n):
        return CommentFactory.create_batch(n, snippet=snippet)
    return create_comment_to_snippet


@pytest.mark.django_db
def test_create_comments(snippet, comment_factory):
    comment_factory(snippet=snippet, n=6)

    assert Comment.objects.count() == 6
    for comment in Comment.objects.all():
        assert comment.snippet == snippet