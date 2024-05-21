from django.urls import path
from groups.views import *

urlpatterns = [
    path('', GroupsShow.as_view(), name='groups'),
    path('<int:group>/', GroupShow.as_view(), name='group'),
    path('create/', CreateGroup.as_view(), name='create_group'),
    path('<int:group>/edit/', UpdateGroup.as_view(), name='edit_group'),
    path('<int:group>/delete/', DeleteGroup.as_view(), name='delete_group'),

]
