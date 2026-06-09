from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.urls import reverse
from rest_framework import viewsets, permissions
from .models import Todo
from .serializers import TodoSerializer
from .forms import TodoForm


class TodoViewSet(viewsets.ModelViewSet):
    """API endpoint for todos. Protected: requires authentication."""
    queryset = Todo.objects.all().order_by("-created_at")
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]


# alias to satisfy older expectation for ExpenseViewSet
ExpenseViewSet = TodoViewSet


def todo_list(request: HttpRequest) -> HttpResponse:
    todos = Todo.objects.all().order_by("-created_at")
    return render(request, "todo/todo_list.html", {"todos": todos})


def todo_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save()
            messages.success(request, "Todo created successfully.")
            return redirect(reverse("todos:todo_list"))
    else:
        form = TodoForm()
    return render(request, "todo/todo_form.html", {"form": form})


def todo_update(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, "Todo updated successfully.")
            return redirect(reverse("todos:todo_list"))
    else:
        form = TodoForm(instance=todo)
    return render(request, "todo/todo_form.html", {"form": form, "todo": todo})


def todo_delete(request: HttpRequest, pk: int) -> HttpResponse:
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        todo.delete()
        messages.success(request, "Todo deleted.")
        return redirect(reverse("todos:todo_list"))
    return render(request, "todo/todo_confirm_delete.html", {"todo": todo})
