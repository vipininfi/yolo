from typing import Any
from .models import ToDo


def create_todo(**kwargs: Any) -> ToDo:
    todo = ToDo.objects.create(**kwargs)
    return todo


def update_todo(instance: ToDo, **kwargs: Any) -> ToDo:
    for key, value in kwargs.items():
        setattr(instance, key, value)
    instance.save()
    return instance


def delete_todo(instance: ToDo) -> None:
    instance.delete()


def toggle_todo(instance: ToDo) -> ToDo:
    instance.completed = not instance.completed
    instance.save()
    return instance
