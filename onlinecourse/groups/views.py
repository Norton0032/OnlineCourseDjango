from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from groups.forms import AddGroup, EditGroup
from groups.models import GroupOnCourse


class GroupsShow(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = GroupOnCourse
    template_name = 'groups/groups.html'
    context_object_name = 'grouponcourse'
    paginate_by = 5
    permission_required = 'groups.view_grouponcourse'
    extra_context = {
        'title': 'Группа',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Группа'
        user = self.request.user
        if 'groups.add_grouponcourse' not in user.get_all_permissions():
            context['grouponcourse'] = user.users.all()
        return context

    def get_queryset(self):
        user = self.request.user
        if 'groups.add_grouponcourse' not in user.get_all_permissions():
            queryset = user.users.all()
        else:
            queryset = super().get_queryset()
        return queryset


class GroupShow(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = GroupOnCourse
    template_name = 'groups/group.html'
    pk_url_kwarg = 'group'
    context_object_name = 'group'
    permission_required = 'groups.view_grouponcourse'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Группа'
        context['name'] = context['group'].name
        context['course'] = context['group'].course
        context['users'] = context['group'].users.all()
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context

    def dispatch(self, request, *args, **kwargs):
        users_in_group = self.get_object().users.all()
        user = request.user
        if 'groups.add_grouponcourse' not in user.get_all_permissions() and user not in users_in_group:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CreateGroup(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = AddGroup
    template_name = 'groups/create.html'
    success_url = reverse_lazy('groups')  # reverse строит маршрут по имени
    extra_context = {
        'title': 'Создание группы',
    }
    permission_required = 'groups.add_grouponcourse'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context


class UpdateGroup(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = GroupOnCourse
    form_class = EditGroup
    pk_url_kwarg = 'group'
    template_name = 'groups/create.html'
    success_url = reverse_lazy('groups')
    extra_context = {
        'title': 'Редактирование группы',
    }
    permission_required = 'groups.change_grouponcourse'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context

    def dispatch(self, request, *args, **kwargs):
        users_in_group = self.get_object().users.all()
        user = request.user
        if 'groups.add_grouponcourse' not in user.get_all_permissions() and user not in users_in_group:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DeleteGroup(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = GroupOnCourse
    fields = '__all__'
    pk_url_kwarg = 'group'
    template_name = 'groups/delete.html'
    success_url = reverse_lazy("groups")
    extra_context = {
        'title': 'Удаление группы',
    }
    permission_required = 'groups.delete_grouponcourse'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context
