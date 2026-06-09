from django.contrib import admin
from .models import ToDo


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "completed", "created_at", "updated_at")
    list_filter = ("completed",)
    search_fields = ("title", "description")
