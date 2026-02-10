from django.contrib import admin
from .models import User, Project, ProjectMember, Sprint, Label, Task, TaskComment, Notification, TaskHistory, TaskAttachment
# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(Sprint)
admin.site.register(Label)
admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(Notification)
admin.site.register(TaskHistory)
admin.site.register(TaskAttachment)