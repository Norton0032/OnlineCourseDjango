from django.urls import path
from application.views import *

urlpatterns = [
    path('create/', CreateApplication.as_view(), name='create_app'),
    path('<int:application>/delete/', DeleteApplication.as_view(), name='delete_app'),
    path('', ApplicationsShow.as_view(), name='apps'),
]
