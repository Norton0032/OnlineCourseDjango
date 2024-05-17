from django.contrib import admin

from course.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price')
    list_editable = ('name', 'price')


# admin.site.register(Course)

