from django.contrib import admin

from groups.models import GroupOnCourse


@admin.register(GroupOnCourse)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course')
    list_editable = ('name', 'course')
