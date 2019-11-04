from django.contrib import admin
from core.models import (
    Sprint, Developer, TaskType, Story, StoryTaskType, Impedment, BugTask
)

# Register your models here.

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    pass

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    pass

@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    pass

@admin.register(StoryTaskType)
class StoryTaskTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Impedment)
class ImpedmentAdmin(admin.ModelAdmin):
    pass

@admin.register(BugTask)
class BugTaskAdmin(admin.ModelAdmin):
    pass