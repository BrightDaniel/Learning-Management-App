from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from students.models import PendingStudent

@login_required
def admin_manage_students(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    # Get the counts for approved and pending students
    pending_students_count = PendingStudent.objects.count()
    approved_students_count = User.objects.filter(groups__name='Student').count()
    total_students_count = pending_students_count + approved_students_count


    context = {
        'pending_students_count': pending_students_count,
        'approved_students_count': approved_students_count,
        'total_students_count': total_students_count
    }

    return render(request, 'admin_manage_students.html', context)
