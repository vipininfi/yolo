from django.db import models


PRIORITY_CHOICES = (
    (1, "High"),
    (2, "Normal"),
    (3, "Low"),
)


class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # New fields
    due_date = models.DateField(null=True, blank=True)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES, default=2)

    class Meta:
        app_label = "todos"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
