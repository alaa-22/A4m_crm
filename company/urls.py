from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "company"
urlpatterns = [
                  path('dashboard/', views.dashboard, name="dashboard"),
                  path('company_home/', views.company_list, name="company_home"),
                  path('add_company/', views.add_company, name="add_company"),
                  path('edit_company/<int:pk>', views.edit_company, name="edit_company"),
                  path('company_profile/<int:pk>/', views.company_profile, name="company_profile"),
                  path('delete_company/<int:pk>', views.delete_company, name="delete_company"),
                  path('delete_company/<int:pk>', views.delete_company, name="delete_company"),
                  # path('create_pdf/', views.render_pdf_view, name='create_pdf'),
                  path('company_report/',views.company_report,name="company_report")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
