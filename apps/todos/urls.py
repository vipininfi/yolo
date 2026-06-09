from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "todos"

router = routers.DefaultRouter()
router.register(r"todos", views.TodoViewSet, basename="todo")

urlpatterns = [
    path("", views.TodoListView.as_view(), name="list"),
    path("create/", views.TodoCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.TodoUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.TodoDeleteView.as_view(), name="delete"),
    path("<int:pk>/toggle/", views.TodoToggleCompleteView.as_view(), name="toggle"),
    path("api/", include((router.urls, "api"), namespace="api")),
]
