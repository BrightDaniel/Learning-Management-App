from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Class

def teacher_manage_class(request):
    # Ensure only teachers can access
    if not request.user.groups.filter(name='Teacher').exists():
        messages.error(request, "Access denied! Only teachers can manage classes.")
        return redirect('teacher_dashboard')

    # Fetch all classes created by the teacher
    classes = Class.objects.filter(teacher=request.user)

    return render(request, 'teacher_manage_class.html', {'classes': classes})
