from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, todo_list, todo_create, todo_update, todo_delete

app_name = "todos"

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('', todo_list, name='todo_list'),
    path('create/', todo_create, name='todo_create'),
    path('<int:pk>/edit/', todo_update, name='todo_update'),
    path('<int:pk>/delete/', todo_delete, name='todo_delete'),
]

# include router URLs for API
urlpatterns += router.urls
