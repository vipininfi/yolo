from typing import Optional, Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.db.models.query import QuerySet
from apps.todos.models import Todo
from apps.todos.forms import TodoForm
from apps.todos.services import get_all_todos
from apps.todos import services

# DRF imports
from rest_framework import viewsets, permissions
from apps.todos.serializers import TodoSerializer

# Template paths used by this module:
#   todos/list.html        — todo list view
#   todos/form.html        — todo create/edit view
#   todos/confirm_delete.html — todo delete view


class TodoListView(ListView):
    model = Todo
    template_name = "todos/list.html"
    context_object_name = "todos"
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet:
        q: Optional[str] = self.request.GET.get("q")
        completed_raw: Optional[str] = self.request.GET.get("completed")

        completed: Optional[bool]
        if completed_raw is None or completed_raw.lower() == "all":
            completed = None
        elif completed_raw.lower() in {"true", "1"}:
            completed = True
        elif completed_raw.lower() in {"false", "0"}:
            completed = False
        else:
            completed = None

        return get_all_todos(q=q, completed=completed)


class TodoCreateView(CreateView):
    model = Todo
    form_class = TodoForm
    template_name = "todos/form.html"
    success_url = reverse_lazy("todos:list")


class TodoUpdateView(UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = "todos/form.html"
    success_url = reverse_lazy("todos:list")


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = "todos/confirm_delete.html"
    success_url = reverse_lazy("todos:list")


class TodoToggleCompleteView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        todo = get_object_or_404(Todo, pk=pk)
        services.toggle_todo_completed(todo)
        return redirect("todos:list")


class TodoViewSet(viewsets.ModelViewSet):
    """API ViewSet for Todo objects."""
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> Any:
        # No user relation on Todo model; restrict to all if authenticated, else none.
        user = getattr(self.request, "user", None)
        if user and user.is_authenticated:
            return Todo.objects.all()
        return Todo.objects.none()
