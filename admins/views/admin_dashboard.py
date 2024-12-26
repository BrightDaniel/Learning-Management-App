from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from teachers.models import Class, PendingTeacher
from students.models import PendingStudent

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    # Query the database for teacher statistics
    approved_teachers = User.objects.filter(groups__name='Teacher', is_active=True)
    pending_teachers = PendingTeacher.objects.all()

    # Count all teachers
    all_teachers = approved_teachers.count() + pending_teachers.count()

    # Total classes
    total_classes = Class.objects.count()

    # Query the database for student statistics
    pending_students = PendingStudent.objects.count()
    approved_students = User.objects.filter(groups__name='Student').count()
    total_students = pending_students + approved_students

    # Total users in the app
    total_users = User.objects.count() + PendingStudent.objects.count()

    context = {
        'approved_teachers': all_teachers,
        'total_classes': total_classes,
        'total_students': total_students,  # Total students (pending + approved)
        'total_users': total_users,  # Total users (approved + pending)
    }

    return render(request, 'admin_dashboard.html', context)
