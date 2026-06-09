from django.contrib import admin
from apps.todos.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "completed", "created_at")
    list_filter = ("completed",)
    search_fields = ("title", "description")
