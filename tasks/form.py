from django import forms
from .models import TaskModel, MeetingModel, SendEmailModel, WhatsappModel, CallModel, NoteModel,ActivityModel


class Taskform(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = '__all__'


class Noteform(forms.ModelForm):
    class Meta:
        model = NoteModel
        fields = '__all__'


class Emailform(forms.ModelForm):
    class Meta:
        model = SendEmailModel
        fields = '__all__'
        exclude = ['made_by', 'email']


class Meetingform(forms.ModelForm):
    class Meta:
        model = MeetingModel
        fields = '__all__'


class Callform(forms.ModelForm):
    class Meta:
        model = CallModel
        fields = '__all__'


class Whatsappform(forms.ModelForm):
    class Meta:
        model = WhatsappModel
        fields = '__all__'


class Activityform(forms.ModelForm):
    class Meta:
        model = ActivityModel
        fields = '__all__'