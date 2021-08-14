from django.contrib import admin
from .models import TaskModel, MeetingModel, SendEmailModel, NoteModel, CallModel,ActivityModel

# Register your models here.
admin.site.register(TaskModel)
admin.site.register(MeetingModel)
admin.site.register(SendEmailModel)
admin.site.register(CallModel)
admin.site.register(NoteModel)
admin.site.register(ActivityModel)
