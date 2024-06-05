from django import forms

from application.models import Application
from course.models import Course
from users.models import User


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['course']
        labels = {
            'course': 'Курс',
        }
        widgets = {
            'course': forms.Select(attrs={'class': 'select-input'}),
        }


class ApplicationDeleteForm(forms.Form):
    status = forms.ChoiceField(choices=[('Одобрить', 'Одобрить'), ('Отклонить', 'Отклонить')],
                               label='Статус заявки', widget=forms.Select(attrs={'class': 'select-input'}))

