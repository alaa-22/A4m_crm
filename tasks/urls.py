from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path("task_list/", views.tasks_list, name="Task list"),
    path("add_task/", views.add_task, name="add Task"),
    path("view_task/<int:pk>", views.view_task, name="view Task"),
    path("delete_task/<int:pk>", views.delete_task, name="delete_task"),
    path("add_email/", views.sendmail, name="send email"),
    path("mail_list/", views.mail_list, name="mail_list"),
    path("add_reminder/", views.add_reminder, name="add_remiend"),
    path("view_mail/<int:pk>", views.view_mail, name="mail_view"),

    path("send_whatsapp/", views.send_whatsapp, name="send_whatsapp"),
    path("send_whatsapp/list/", views.whats_list, name="whats_list"),
    path("add_meeting_details/", views.add_meeting, name="add_meeting"),
    path("list_meetings_detail/", views.list_meeting, name="list_meeting"),
    path("view_meeting/<int:pk>", views.view_meeting, name="meeting_view"),

    path("add_call_details/", views.add_call, name="add_call"),
    path("list_calls_detail/", views.list_call, name="list_call"),
    path("view_call/<int:pk>", views.view_call, name="call_view"),
    path("activity_list/", views.list_activity1, name="activity_list"),
    path("add_note/",views.add_note,name="add_note"),

    path("calender/", views.calender, name="calender"),

]
