from django.db import models

from course.models import Course
from users.models import User


class GroupOnCourse(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True, null=True, related_name='users')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
