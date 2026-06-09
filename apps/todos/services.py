from typing import Optional
from django.db.models import Q
from django.db.models.query import QuerySet
from apps.todos.models import Todo


def get_all_todos(q: Optional[str] = None, completed: Optional[bool] = None) -> QuerySet:
    """Return a QuerySet of Todos, optionally filtered by search query and completion status.

    - q: case-insensitive search across title and description
    - completed: True/False to filter by completed status, or None to not filter

    Preserves model default ordering declared in Todo.Meta.ordering.
    """
    qs: QuerySet = Todo.objects.all()

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    if completed is not None:
        qs = qs.filter(completed=completed)

    return qs


def toggle_todo_completed(todo: Todo) -> None:
    """Toggle the completed flag on a Todo and save it."""
    todo.completed = not todo.completed
    todo.save()
