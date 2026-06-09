from django import forms
from apps.todos.models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
