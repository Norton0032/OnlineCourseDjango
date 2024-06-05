from django.contrib import admin

from application.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    list_editable = ('course',)
