from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "status"]
    
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter title",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter description",
                "rows": 4,
            }),
            "status": forms.Select(attrs={
                "class": "form-control",
            }),
        }