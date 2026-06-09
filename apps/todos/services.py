from typing import Iterable
from apps.todos.models import Todo


def get_all_todos() -> Iterable[Todo]:
    return Todo.objects.all()


def toggle_todo_completed(todo: Todo) -> None:
    todo.completed = not todo.completed
    todo.save()
