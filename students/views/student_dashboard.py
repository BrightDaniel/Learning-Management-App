from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from teachers.models import Course

@login_required
def student_dashboard(request):
    # Ensure only students can access
    if not request.user.groups.filter(name="Student").exists():
        messages.error(request, "Access denied! Only students can access the dashboard.")
        return redirect("student_login")
    
    student_profile = request.user.profile
    student_class = student_profile.student_class if student_profile else None

    # Get courses for the student's class
    courses = []
    if student_class:
        courses = Course.objects.filter(associated_class=student_class).prefetch_related('weekly_lessons__quiz')

    # Prepare course data with lesson and quiz counts
    course_data = [
        {
            "id": course.id,  
            "name": course.name,
            "description": course.description,
            "teacher": course.teacher.get_full_name(),
            "weekly_lesson_count": course.weekly_lessons.count(),
            "quiz_count": sum(1 for lesson in course.weekly_lessons.all() if hasattr(lesson, 'quiz')),
        }
        for course in courses
    ]

    context = {
        "student_name": request.user.get_full_name() or request.user.username,
        "student_email": request.user.email,
        "student_class": student_class,
        "course_data": course_data,
    }

    return render(request, "student_dashboard.html", context)
