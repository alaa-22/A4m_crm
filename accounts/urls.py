from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
app_name = "account"
urlpatterns = [
                  path('', views.test, name="landing page"),
                  path('login/', views.login1, name="account_login"),
                  path('logout/', views.logout_fun, name="logout"),
                  path('add_user/', views.add_user, name="add_user"),
                  path('user_list/', views.list_users, name="list_user"),
                  path('edit_user/<int:pk>', views.edit_user, name="edit_user"),
                  path('delete_user/<int:pk>', views.delete_user, name="delete_user"),
                  path('add_group/', views.add_group, name="add_group"),
                  path('add_user_perms/', views.add_user_perm, name="add_user_perms"),
                  path('list_user_perms/', views.list_user_perms, name="list_user_perms"),
                  path('edit_user_perms/<int:pk>', views.edit_user_perms, name="edit_user_perms"),
                  path('list_group/', views.list_groups, name="list_group"),
                  path('delete_group/<int:pk>', views.delete_group, name="delete_group"),
                  path('edit_group/<int:pk>', views.edit_group, name="edit_group"),
                  path('profile/<int:pk>', views.edit_profile, name="profile"),
                  path('user_activity/<int:name>', views.user_activity, name="user_activity"),
                  path('site_setting/', views.site_setting, name="site_setting"),
                  path('system_logs/', views.system_logs, name="system_logs"),
                  path('system_logs_details/<int:pk>', views.system_log_details, name="system_log_details"),
                  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
