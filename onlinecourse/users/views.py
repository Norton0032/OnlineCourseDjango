from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from onlinecourse import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, CreateUserForm, \
    UpdateUserForm
from users.models import User


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {
        'title': 'Регистрация'
    }
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        student_group = Group.objects.get(name='student')
        student_group.user_set.add(user)
        return super().form_valid(form)


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': 'Профиль',
        'default_img': settings.DEFAULT_USER_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user



class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "users/password_change_form.html"


class UsersShow(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'users/crud/users.html'
    context_object_name = 'users'
    paginate_by = 5
    permission_required = 'users.view_user'
    extra_context = {
        'title': 'Список пользователей'
    }

    def get_queryset(self):
        user = self.request.user

        if 'groups.add_grouponcourse' not in user.get_all_permissions():
            groups = user.users.all()
            queryset = User.objects.filter(users__in=groups).distinct()
        else:
            queryset = super().get_queryset()
        return queryset


class UserShow(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'users/crud/user.html'
    pk_url_kwarg = 'user'
    context_object_name = 'selected_user'
    permission_required = 'groups.change_grouponcourse'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователь'
        context['first_name'] = context['selected_user'].first_name if context[
            'selected_user'].first_name else 'нет имени'
        context['last_name'] = context['selected_user'].last_name if context[
            'selected_user'].last_name else 'нет фамилии'
        context['photo'] = context['selected_user'].photo
        context['username'] = context['selected_user'].username
        context['email'] = context['selected_user'].email if context['selected_user'].email else 'нет почты'
        context['date_birth'] = context['selected_user'].date_birth if context[
            'selected_user'].date_birth else 'не задан день рождения'
        context['grouponcourse'] = context['selected_user'].users.all()
        context['role'] = ' '.join(map(str, context['selected_user'].groups.all()))
        context['default_img'] = settings.DEFAULT_USER_IMAGE
        context['button_prev'] = self.request.META.get('HTTP_REFERER')

        return context

    def dispatch(self, request, *args, **kwargs):
        groups_select_user = self.get_object().users.all()
        user = request.user
        groups_auth_user = user.users.all()
        print(set(groups_select_user) & set(groups_auth_user))
        if 'groups.add_grouponcourse' not in user.get_all_permissions() and not (
                set(groups_select_user) & set(groups_auth_user)):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CreateUser(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'users/crud/create.html'
    success_url = reverse_lazy('users')  # reverse строит маршрут по имени
    extra_context = {
        'title': 'Создание пользователя',
    }
    permission_required = 'users.add_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context


class UpdateUser(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UpdateUserForm
    pk_url_kwarg = 'user'
    template_name = 'users/crud/create.html'
    context_object_name = 'selected_user'
    success_url = reverse_lazy('users')  # reverse строит маршрут по имени
    extra_context = {
        'title': 'Редактирование пользователя',
    }
    permission_required = 'users.change_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context


class DeleteUser(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = get_user_model()
    fields = '__all__'
    pk_url_kwarg = 'user'
    template_name = 'users/crud/delete.html'
    context_object_name = 'selected_user'
    success_url = reverse_lazy("users")
    extra_context = {
        'title': 'Удаление пользователя',
    }
    permission_required = 'users.delete_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_prev'] = self.request.META.get('HTTP_REFERER')
        return context
