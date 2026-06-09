from typing import Iterable, List
from django.db import transaction
from apps.todos.models import Todo


def get_all_todos() -> Iterable[Todo]:
    return Todo.objects.all()


def toggle_todo_completed(todo: Todo) -> None:
    todo.completed = not todo.completed
    todo.save()


def bulk_toggle_completed(todo_ids: List[int]) -> int:
    """Toggle completion for multiple todos by ids and return number updated."""
    if not todo_ids:
        return 0

    updated = 0
    with transaction.atomic():
        todos = list(Todo.objects.filter(id__in=todo_ids))
        for todo in todos:
            todo.completed = not todo.completed
            todo.save()
            updated += 1
    return updated
