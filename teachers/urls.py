from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher_signup/', views.teacher_registeration, name='teacher_registeration'),
    path('teacher_signin/', views.teacher_login, name='teacher_login'),
    path('teacher_forgot_password/', views.teacher_forgot_password, name='teacher_forgot_password'),
    path('teacher_reset_password_code/', views.teacher_reset_password_code, name='teacher_reset_password_code'),
    path('teacher_reset_password/', views.teacher_reset_password, name='teacher_reset_password'),  
    path('teacher_create_class/', views.teacher_create_class, name='teacher_create_class'),
    path('teacher_manage_class/', views.teacher_manage_class, name='teacher_manage_class'),  
    path('teacher_settings/', views.teacher_settings, name='teacher_settings'),
    path('teacher_logout', views.teacher_logout, name='teacher_logout'),
    path('teacher_create_course', views.teacher_create_course, name='teacher_create_course'),
    path('teacher_manage_courses/', views.teacher_manage_courses, name='teacher_manage_courses'), 
    path('edit_course/<int:course_id>/', views.edit_course_details, name='edit_course_details'),
    path('edit-weekly-content/<int:content_id>/', views.edit_weekly_content, name='edit_weekly_content'),
    path('weekly-content/<int:content_id>/delete/', views.delete_weekly_content, name='delete_weekly_content'),
    # path('add_quiz_question/<int:quiz_id>/add-question/', views.add_quiz_question, name='add_quiz_question'),
    # path('publish_quiz/<int:quiz_id>/', views.publish_quiz, name='publish_quiz'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('view-course-grades/', views.teacher_view_course_grades, name='teacher_view_course_grades'),
    path('view-grade/<int:course_id>/', views.teacher_view_grade, name='teacher_view_grade'),
    path('edit-class/<int:class_id>/', views.teacher_edit_class, name='teacher_edit_class'),

    



]

