from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        app_label = "todos"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
