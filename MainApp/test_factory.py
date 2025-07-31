import pytest
from .factories import *
from .models import User

@pytest.mark.django_db
def test_task1():
    UserFactory(username="Alice")
    user = User.objects.get(username="Alice")

    assert user.username == "Alice"


@pytest.mark.django_db
def test_task2():
    tags = TagFactory.create_batch(5)

    assert Tag.objects.count() == 5
    assert len(tags) == 5


@pytest.mark.django_db
def test_task3():
