from django.test import Client
from django.urls import reverse
from apps.todos.models import Todo


def test_todo_model_creation(db) -> None:
    todo = Todo.objects.create(title='Test', description='desc')
    assert todo.pk is not None
    assert todo.title == 'Test'
    assert not todo.completed


def test_todo_list_view(client: Client) -> None:
    Todo.objects.create(title='List item', description='x')
    url = reverse('todos:list')
    response = client.get(url)
    assert response.status_code == 200
    assert b'List item' in response.content
