from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from ..models import Class, Course
from django.contrib.auth.models import User


@login_required
def teacher_dashboard(request):
    # Ensure only teachers can access
    if not request.user.groups.filter(name='Teacher').exists():
        messages.error(request, "Access denied! Only teachers can access the dashboard.")
        return redirect('teacher_login')

    # Count the classes and courses
    class_count = Class.objects.filter(teacher=request.user).count()
    course_count = Course.objects.filter(teacher=request.user).count()

    # Get all students in the teacher's classes
    teacher_classes = Class.objects.filter(teacher=request.user).prefetch_related('students')
    students = User.objects.filter(profile__student_class__in=teacher_classes).distinct()

    context = {
        'teacher_name': request.user.get_full_name() or request.user.username,
        'teacher_email': request.user.email,
        'class_count': class_count,
        'course_count': course_count,
        'student_count': students.count(),
        'students': students,  # Pass the student list to the template
    }

    return render(request, 'teacher_dashboard.html', context)
