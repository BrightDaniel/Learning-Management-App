from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from teachers.models import Class, Course

@login_required
def admin_manage_classes(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    # Fetch all classes
    classes = Class.objects.select_related('teacher').all()

    # Handle delete request
    if request.method == "POST" and 'delete_class_id' in request.POST:
        class_id = request.POST.get('delete_class_id')
        cls = get_object_or_404(Class, id=class_id)
        cls.delete()
        messages.success(request, "Class deleted successfully.")
        return redirect('admin_manage_classes')

    return render(request, 'admin_manage_classes.html', {'classes': classes})


@login_required
def admin_class_details(request, class_id):
    if not request.user.is_superuser:
        return redirect('admin_login')

    cls = get_object_or_404(Class, id=class_id)
    courses = Course.objects.filter(associated_class=cls)

    # Handle course deletion
    if request.method == "POST" and 'delete_course_id' in request.POST:
        course_id = request.POST.get('delete_course_id')
        course = get_object_or_404(Course, id=course_id)
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect('admin_class_details', class_id=class_id)

    return render(request, 'admin_class_details.html', {'class': cls, 'courses': courses})
