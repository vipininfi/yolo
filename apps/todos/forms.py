from django import forms
from apps.todos.models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "completed", "due_date", "priority"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
        }
