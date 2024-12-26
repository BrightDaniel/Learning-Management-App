from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render, redirect
from ..models import Class, Course


def teacher_dashboard(request):
    # Ensure only teachers can access
    if not request.user.groups.filter(name='Teacher').exists():
        messages.error(request, "Access denied! Only teachers can access the dashboard.")
        return redirect('teacher_login')  

    class_count = Class.objects.filter(teacher=request.user).count()
    course_count = Course.objects.filter(teacher=request.user).count()

    context = {
        'teacher_name': request.user.get_full_name() or request.user.username,  
        'teacher_email': request.user.email, 
        'class_count': class_count,
        'course_count': course_count,  
    }

    return render(request, 'teacher_dashboard.html', context)
