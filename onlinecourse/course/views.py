from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import AddCourse
from .models import Course


class CoursesShow(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    template_name = 'course/courses.html'
    context_object_name = 'courses'
    extra_context = {
        'title': 'Список курсов'
    }
    paginate_by = 5
    permission_required = 'course.view_course'


class CourseShow(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Course
    template_name = 'course/course.html'
    pk_url_kwarg = 'course'
    context_object_name = 'course'
    permission_required = 'course.view_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Курс'
        context['name'] = context['course'].name
        context['description'] = context['course'].description
        context['price'] = context['course'].price
        context['grouponcourse'] = context['course'].grouponcourse_set.all()
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context




class CreateCourse(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = AddCourse
    template_name = 'course/create.html'
    success_url = reverse_lazy('courses')  # reverse строит маршрут по имени
    extra_context = {
        'title': 'Создание курса',
    }
    permission_required = 'course.add_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context


class UpdateCourse(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Course
    fields = '__all__'
    pk_url_kwarg = 'course'
    template_name = 'course/create.html'
    success_url = reverse_lazy('courses')  # reverse строит маршрут по имени
    extra_context = {
        'title': 'Редактирование курса',
    }
    permission_required = 'course.change_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context


class DeleteCourse(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    fields = '__all__'
    pk_url_kwarg = 'course'
    template_name = 'course/delete.html'
    success_url = reverse_lazy("courses")
    extra_context = {
        'title': 'Удаление курса',
    }
    permission_required = 'course.delete_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена")
