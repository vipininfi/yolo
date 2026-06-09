from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "todos"

# HTML views
urlpatterns = [
    path("", views.todo_list, name="list"),
    path("create/", views.todo_create, name="create"),
    path("<int:pk>/edit/", views.todo_edit, name="edit"),
    path("<int:pk>/delete/", views.todo_delete, name="delete"),
    path("<int:pk>/toggle/", views.todo_toggle, name="toggle"),
]

# API router for DRF ViewSet
router = DefaultRouter()
router.register(r"api/todos", views.ToDoViewSet, basename="todo")

# append router-generated API routes
urlpatterns += router.urls
