from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from application.forms import ApplicationForm, ApplicationDeleteForm
from application.models import Application
from onlinecourse.settings import EMAIL_HOST_USER


class CreateApplication(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = ApplicationForm
    template_name = 'application/create.html'
    success_url = reverse_lazy('courses')  # reverse строит маршрут по имени
    extra_context = {
        'title': 'Создание заявки на курс',
    }
    permission_required = 'users.view_user'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context


class ApplicationsShow(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Application
    template_name = 'application/applications.html'
    context_object_name = 'applications'
    extra_context = {
        'title': 'Список заявок на курс'
    }
    paginate_by = 5
    permission_required = 'users.view_user'

    def get_queryset(self):
        user = self.request.user
        if 'users.delete_user' not in user.get_all_permissions():
            queryset = super().get_queryset().filter(user=user)
        else:
            queryset = super().get_queryset()
        return queryset


class DeleteApplication(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Application
    form_class = ApplicationDeleteForm
    fields = '__all__'
    pk_url_kwarg = 'application'
    template_name = 'application/delete.html'
    success_url = reverse_lazy("apps")
    extra_context = {
        'title': 'Обработка заявки',
    }
    permission_required = 'users.delete_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        context['user'] = context['application'].user.username
        context['course'] = context['application'].course.name
        return context

    def form_valid(self, form):
        application = self.get_object()
        status = form.cleaned_data['status']
        user_email = application.user.email
        if status == 'Одобрить':
            subject = 'Ваша заявка одобрена'
            message = f'Здравствуйте, {application.user.username}. Ваша заявка на курс {application.course.name} была одобрена.'
        elif status == 'Отклонить':
            subject = 'Ваша заявка отклонена'
            message = f'Здравствуйте, {application.user.username}. Ваша заявка на курс {application.course.name} была отклонена.'
        send_mail(subject, message, EMAIL_HOST_USER, [user_email], fail_silently=False)
        return super().form_valid(form)
