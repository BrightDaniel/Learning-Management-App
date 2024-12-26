from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from ..models import Class, Course

@login_required
def teacher_create_course(request):
    # Ensure only teachers can access
    if not request.user.groups.filter(name='Teacher').exists():
        messages.error(request, "Access denied! Only teachers can create courses.")
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_description = request.POST.get('course_description')
        class_id = request.POST.get('class_id')

        # Validate inputs
        if not course_name or not class_id:
            messages.error(request, "Course name and class association are required.")
            return redirect('teacher_create_course')

        # Check if class belongs to the teacher
        try:
            associated_class = Class.objects.get(id=class_id, teacher=request.user)
        except Class.DoesNotExist:
            messages.error(request, "Invalid class selection.")
            return redirect('teacher_create_course')

        # Create the course
        Course.objects.create(
            name=course_name,
            description=course_description,
            teacher=request.user,
            associated_class=associated_class,
        )
        messages.success(request, f"Course '{course_name}' created successfully!")
        return redirect('teacher_dashboard')

    # Fetch only classes created by the logged-in teacher
    classes = Class.objects.filter(teacher=request.user)

    return render(request, 'teacher_create_course.html', {'classes': classes})
