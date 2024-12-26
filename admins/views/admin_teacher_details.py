from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from teachers.models import Class
from django.contrib.auth.models import User

@login_required
def admin_teacher_details(request, teacher_id):
    if not request.user.is_superuser:
        return redirect('admin_login')

    teacher = get_object_or_404(User, id=teacher_id)
    assigned_classes = Class.objects.filter(teacher=teacher)

    if request.method == "POST":
        class_id = request.POST.get('class_id')
        new_teacher_id = request.POST.get('new_teacher_id')

        if "reassign" in request.POST:
            new_teacher = get_object_or_404(User, id=new_teacher_id)
            Class.objects.filter(id=class_id).update(teacher=new_teacher)

        elif "remove" in request.POST:
            Class.objects.filter(id=class_id).update(teacher=None)

        return redirect('admin_teacher_details', teacher_id=teacher.id)

    context = {
        'teacher': teacher,
        'assigned_classes': assigned_classes,
    }

    return render(request, 'admin_teacher_details.html', context)
