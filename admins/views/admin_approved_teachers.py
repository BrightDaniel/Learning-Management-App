'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from teachers.models import Class

@login_required
def admin_approved_teachers(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    if request.method == "POST":
        teacher_id = request.POST.get('teacher_id')
        action = request.POST.get('action')

        teacher = get_object_or_404(User, id=teacher_id)

        if action == "delete":
            # Unassign classes assigned to this teacher
            Class.objects.filter(teacher=teacher).update(teacher=None)
            teacher.delete()
            return redirect('admin_approved_teachers')

        elif action == "view_details":
            # Redirect to teacher details page
            return redirect('admin_teacher_details', teacher_id=teacher.id)

    # Fetch approved teachers using the same logic as admin_manage_teachers
    all_teachers = User.objects.filter(groups__name='Teacher')
    approved_teachers = all_teachers.filter(is_active=True)

    context = {
        'approved_teachers': approved_teachers,
    }

    return render(request, 'admin_approved_teachers.html', context)

'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from teachers.models import Class
from django.contrib.auth.hashers import make_password

@login_required
def admin_approved_teachers(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    if request.method == "POST":
        teacher_id = request.POST.get('teacher_id')
        action = request.POST.get('action')

        teacher = get_object_or_404(User, id=teacher_id)

        if action == "reset":
            # Confirm the reset action (triggered after JS confirmation)
            new_full_name = "Unassigned Teacher"
            new_email = "exampleteacher@gmail.com"
            new_password = "examplepassword"

            # Update teacher's details
            teacher.first_name = new_full_name.split()[0]
            teacher.last_name = " ".join(new_full_name.split()[1:])
            teacher.email = new_email
            teacher.username = new_email  # Make sure email is also the username
            teacher.password = make_password(new_password)  # Hash the new password
            teacher.save()

            messages.success(request, f"Login details for {teacher.get_full_name} have been reset.")

            return redirect('admin_approved_teachers')

        elif action == "view_details":
            return redirect('admin_teacher_details', teacher_id=teacher.id)

    # Fetch approved teachers
    approved_teachers = User.objects.filter(groups__name='Teacher', is_active=True)

    context = {
        'approved_teachers': approved_teachers,
    }

    return render(request, 'admin_approved_teachers.html', context)
