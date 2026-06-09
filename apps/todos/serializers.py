from rest_framework import serializers
from apps.todos.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            "id",
            "title",
            "description",
            "completed",
            "due_date",
            "priority",
            "created_at",
            "updated_at",
        ]
