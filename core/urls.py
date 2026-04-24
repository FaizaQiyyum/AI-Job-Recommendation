from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ---------- Public ----------
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ---------- Jobs ----------
    path('jobs/', views.job_list, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('recommendations/', views.recommendations, name='recommendations'),

    # ---------- Admin ----------
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/jobs/', views.admin_jobs, name='admin_jobs'),
    path('admin/add-job/', views.add_job, name='add_job'),
    path('admin/edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('admin/delete-job/<int:job_id>/', views.delete_job, name='delete_job'),

    # ---------- Admin applications and users ----------
    path('admin/update-status/<int:app_id>/<str:status>/', views.update_application_status, name='update_application_status'),
    path('admin/users/', views.admin_users, name='admin_users'),

    # ---------- User Profile & Applications ----------
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('my-bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('bookmark/<int:job_id>/', views.bookmark_job, name='bookmark_job'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
path('verify-code/', views.verify_code, name='verify_code'),
path('reset-password/', views.reset_password, name='reset_password'),

]
