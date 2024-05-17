from django import forms

from groups.models import GroupOnCourse


class AddGroup(forms.ModelForm):
    class Meta:
        model = GroupOnCourse
        fields = ['name', 'course']
        labels = {
            'course': 'Курс',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'course': forms.Select(attrs={'class': 'select-input'}),
        }


class EditGroup(forms.ModelForm):
    class Meta:
        model = GroupOnCourse
        fields = ['name', 'course', 'users']
        labels = {
            'course': 'Курс',
            'users': 'Участники',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'course': forms.Select(attrs={'class': 'select-input'}),
            'users': forms.SelectMultiple(attrs={'class': 'select-multi-input'}),
        }
