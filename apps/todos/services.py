from typing import Iterable
from django.db.models import QuerySet
from apps.todos.models import Todo, PRIORITY_LOW, PRIORITY_MEDIUM, PRIORITY_HIGH


def get_all_todos() -> Iterable[Todo]:
    """Return all todos ordered by priority (high -> low) then due_date then created_at."""
    priority_order = {PRIORITY_HIGH: 0, PRIORITY_MEDIUM: 1, PRIORITY_LOW: 2}
    # Since Django ORM can't sort by custom mapping directly, we annotate with a case expression
    from django.db.models import Case, When, Value, IntegerField

    return (
        Todo.objects.annotate(
            _priority_order=Case(
                When(priority=PRIORITY_HIGH, then=Value(0)),
                When(priority=PRIORITY_MEDIUM, then=Value(1)),
                When(priority=PRIORITY_LOW, then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        )
        .order_by("_priority_order", "due_date", "-created_at")
        .all()
    )


def toggle_todo_completed(todo: Todo) -> None:
    todo.completed = not todo.completed
    todo.save()
