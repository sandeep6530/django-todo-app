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

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")

        return title
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if self.instance.pk:
            exists = Todo.objects.filter(title__iexact=title, user=self.instance.user).exclude(pk=self.instance.pk).exists()
        else:
            exists = Todo.objects.filter(
                title__iexact=title,
                user=self.initial.get("user")
            ).exists()

        if exists:
            raise forms.ValidationError("You already have a todo with this title")
        
        return cleaned_data