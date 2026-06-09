from typing import Any
from django import forms
from .models import ToDo


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ["title", "description"]

    def save(self, commit: bool = True) -> ToDo:
        instance: ToDo = super().save(commit=False)
        if commit:
            instance.save()
        return instance
