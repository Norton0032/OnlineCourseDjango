from django.urls import path
from course.views import *

urlpatterns = [
    path('', CoursesShow.as_view(), name='courses'),
    path('<int:course>/', CourseShow.as_view(), name='course'),
    path('create/', CreateCourse.as_view(), name='create_course'),
    path('<int:course>/edit/', UpdateCourse.as_view(), name='edit_course'),
    path('<int:course>/delete/', DeleteCourse.as_view(), name='delete_course'),

]
