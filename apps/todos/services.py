from typing import Iterable
from .models import Todo


def list_todos() -> Iterable[Todo]:
    return Todo.objects.all()


def get_todo(pk: int) -> Todo:
    return Todo.objects.get(pk=pk)


def create_todo(**kwargs) -> Todo:
    return Todo.objects.create(**kwargs)


def update_todo(instance: Todo, **kwargs) -> Todo:
    for key, value in kwargs.items():
        setattr(instance, key, value)
    instance.save()
    return instance


def delete_todo(instance: Todo) -> None:
    instance.delete()
