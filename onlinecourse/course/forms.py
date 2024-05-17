from django import forms
from .models import Course


class AddCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'price']
        widgets = {
            forms.Textarea(attrs={'cols': 50, 'rows': 10})
        }

