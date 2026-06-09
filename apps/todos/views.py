from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q
from apps.todos.models import Todo
from apps.todos.forms import TodoForm
from apps.todos import services

# DRF imports
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

# django-filter is optional in some environments; import defensively
try:
    from django_filters.rest_framework import DjangoFilterBackend
except Exception:
    DjangoFilterBackend = None

from apps.todos.serializers import TodoSerializer
from apps.todos.services import bulk_toggle_completed

# Template paths used by this module:
#   todos/list.html        — todo list view
#   todos/form.html        — todo create/edit view
#   todos/confirm_delete.html — todo delete view


class TodoListView(ListView):
    model = Todo
    template_name = "todos/list.html"
    context_object_name = "todos"
    ordering = ["-created_at"]

    def get_queryset(self) -> Any:
        qs = Todo.objects.all()
        q = self.request.GET.get("q")
        priority = self.request.GET.get("priority")
        due_before = self.request.GET.get("due_before")

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if priority:
            try:
                p = int(priority)
                qs = qs.filter(priority=p)
            except (ValueError, TypeError):
                pass
        if due_before:
            try:
                from datetime import datetime

                due_date = datetime.fromisoformat(due_before).date()
                qs = qs.filter(due_date__lte=due_date)
            except (ValueError, TypeError):
                pass
        return qs.order_by("-created_at")


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
    # build filter_backends list but omit DjangoFilterBackend if it's not available
    filter_backends = [b for b in [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] if b]
    filterset_fields = ["priority", "completed", "due_date"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "due_date", "priority"]

    def get_queryset(self) -> Any:
        user = getattr(self.request, "user", None)
        if user and user.is_authenticated:
            return Todo.objects.all().order_by("-created_at")
        return Todo.objects.none()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=["post"])
    def bulk_toggle(self, request: Request) -> Response:
        ids = request.data.get("ids") or request.data.get("ids[]")
        if not isinstance(ids, list):
            return Response({"detail": "ids must be a list of integers."}, status=400)
        try:
            ids = [int(i) for i in ids]
        except (ValueError, TypeError):
            return Response({"detail": "ids must be integers."}, status=400)
        updated = bulk_toggle_completed(ids)
        return Response({"updated": updated})
