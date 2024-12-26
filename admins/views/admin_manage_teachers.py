from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from teachers.models import PendingTeacher

@login_required
def admin_manage_teachers(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    # Query for approved and pending teachers
    approved_teachers = User.objects.filter(groups__name='Teacher', is_active=True)
    pending_teachers = PendingTeacher.objects.all()

    # Count all teachers
    all_teachers_count = approved_teachers.count() + pending_teachers.count()

    context = {
        'all_teachers_count': all_teachers_count,
        'approved_teachers_count': approved_teachers.count(),
        'pending_teachers_count': pending_teachers.count(),
    }

    return render(request, 'admin_manage_teachers.html', context)
