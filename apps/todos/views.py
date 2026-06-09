from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework import viewsets, permissions
from .models import ToDo
from .forms import ToDoForm
from .serializers import ToDoSerializer
from .services import toggle_todo, delete_todo, update_todo, create_todo


# Function-based views for HTML UI
def todo_list(request: HttpRequest) -> HttpResponse:
    todos = ToDo.objects.all().order_by("-created_at")
    form = ToDoForm()
    return render(request, "todos/list.html", {"todos": todos, "form": form})


def todo_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ToDoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("todos:list")
    return redirect("todos:list")


def todo_edit(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == "POST":
        form = ToDoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("todos:list")
    else:
        form = ToDoForm(instance=todo)
    return render(request, "todos/form.html", {"form": form, "todo": todo})


def todo_delete(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == "POST":
        delete_todo(todo)
        return redirect("todos:list")
    return render(request, "todos/form.html", {"form": None, "todo": todo})


def todo_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(ToDo, pk=pk)
    toggle_todo(todo)
    return redirect("todos:list")


# DRF API ViewSet for ToDo
class ToDoViewSet(viewsets.ModelViewSet):
    """API endpoint for ToDo items. Requires authentication."""
    queryset = ToDo.objects.all().order_by("-created_at")
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer: Any) -> None:  # type: ignore[name-defined]
        serializer.save()
