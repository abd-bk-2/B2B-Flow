from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # allow editing the main editable fields; creator should not be changed here
        fields = ['title', 'description', 'amount', 'status', 'receiver']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
