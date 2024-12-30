from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student_register/', views.student_register, name='student_register'),
    path('student_login/', views.student_login, name='student_login'),
    path('student_settings/', views.student_settings, name='student_settings'),
    path('student_logout/', views.student_logout, name='student_logout'),
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    path('course/<int:course_id>/week/<int:week_id>/', views.course_detail, name='course_detail'),
    path('quiz/<int:week_id>/start/', views.start_quiz, name='start_quiz'),
    path('quiz/submit/', views.submit_quiz, name='submit_quiz'),
    path('student_grades/', views.student_grades, name='student_grades')



   
]

