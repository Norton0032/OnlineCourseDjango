from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
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
    return render(request, template_name="statuscode/404.html", context={"title": "Страница не найдена"}, status=404)


def server_error(request):
    return render(request, template_name="statuscode/500.html", context={"title": "Ошибка сервера"}, status=500)


def permission_denied(request, exception):
    return render(request, template_name="statuscode/403.html", context={"title": "Доступ запрещен"}, status=403)


def bad_request(request, exception):
    return render(request, template_name="statuscode/400.html", context={"title": "Запрос отправлен с ошибкой"}, status=400)
