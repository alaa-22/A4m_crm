from django.urls import path

from . import views

app_name = "contact"
urlpatterns = [

    path('contact_home/', views.contact_list, name="contact_home"),
    path('add_contact/', views.add_contact, name="add_contact"),
    path('add_lead/', views.add_lead, name="add_lead"),
    path('lead_list/', views.lead_list, name="list_lead"),
    path('edit_lead/<int:pk>', views.edit_lead, name="edit_lead"),
    path('covert_lead/<int:pk>', views.convert_lead, name="convert_lead"),
    path('edit_contact/<int:pk>', views.edit_contact, name="edit_contact"),
    path('delete_contact/<int:pk>', views.delete_contact, name="delete_contact"),
    path('contact_profile/<int:pk>', views.contact_profile, name="contact_profile"),
    path('delete_lead/<int:pk>', views.delete_lead, name="delete_lead"),
    path('add_product/', views.add_product, name="add_product"),
    path('list_product/', views.list_product, name="list_product"),
    path('contact_report/', views.contact_report, name="contact_report"),
    path('lead_report/', views.lead_report, name="lead_report"),

]
