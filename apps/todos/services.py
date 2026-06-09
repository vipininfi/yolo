from typing import Iterable
from apps.todos.models import Todo


def list_todos() -> Iterable[Todo]:
    return Todo.objects.all()


def toggle_todo_complete(todo: Todo) -> Todo:
    todo.completed = not todo.completed
    todo.save()
    return todo
