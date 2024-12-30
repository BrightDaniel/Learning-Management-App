from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin_settings/', views.admin_settings, name='admin_settings'),
    
    path('admin_pending_teachers/', views.admin_pending_teachers, name='admin_pending_teachers'),
    path('admin_manage_teachers/', views.admin_manage_teachers, name='admin_manage_teachers'),
    path('admin_approved_teachers/', views.admin_approved_teachers, name='admin_approved_teachers'),
    
    path('admin_manage_students/', views.admin_manage_students, name='admin_manage_students'),
    path('admin_pending_students/', views.admin_pending_students, name='admin_pending_students'),
    path('admin_approved_students/', views.admin_approved_students, name='admin_approved_students'),

    path('admin_manage_classes/', views.admin_manage_classes, name='admin_manage_classes'),

    path('admin_teacher_details/<int:teacher_id>/', views.admin_teacher_details, name='admin_teacher_details'),

    path('all_users/', views.all_users, name='all_users'),
    path('admin/class/<int:class_id>/details/', views.admin_class_details, name='admin_class_details'),



    
  

]