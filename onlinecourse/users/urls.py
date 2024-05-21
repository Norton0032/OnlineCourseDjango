from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from . import views
from .forms import MyPasswordResetForm

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('', views.ProfileUser.as_view(), name='profile'),
    path('password-change/', views.UserPasswordChange.as_view(), name='password-change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password-reset/',
         PasswordResetView.as_view(template_name='users/password_reset_form.html', form_class=MyPasswordResetForm),
         name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('users/', views.UsersShow.as_view(), name='users'),
    path('users/<int:user>/', views.UserShow.as_view(), name='user'),
    path('users/create/', views.CreateUser.as_view(), name='create_user'),
    path('users/<int:user>/edit/', views.UpdateUser.as_view(), name='edit_user'),
    path('users/<int:user>/delete/', views.DeleteUser.as_view(), name='delete_user')
]
