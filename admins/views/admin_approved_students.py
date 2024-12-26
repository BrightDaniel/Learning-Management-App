from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages


@login_required
def admin_approved_students(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        action = request.POST.get('action')

        try:
            student = User.objects.get(id=student_id)

            if action == 'delete':
                # Delete the student and their profile
                student.profile.delete()
                student.delete()
                messages.success(request, f"Student {student.get_full_name()} has been deleted successfully.")
            else:
                messages.error(request, "Invalid action.")
        except User.DoesNotExist:
            messages.error(request, "Student not found.")

    # Fetch all students in the 'Student' group with their profiles
    student_group = Group.objects.get(name="Student")
    approved_students = User.objects.filter(groups=student_group).select_related('profile')
    

    return render(request, 'admin_approved_students.html', {'approved_students': approved_students})
