from django.contrib import admin
from apps.todos.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "completed", "created_at")
    search_fields = ("title", "description")
    list_filter = ("completed",)
