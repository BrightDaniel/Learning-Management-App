from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User, Group  
from students.models import PendingStudent
from students.models import StudentProfile


@login_required
def admin_pending_students(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        action = request.POST.get('action')

        try:
            student = PendingStudent.objects.get(id=student_id)

            if action == 'approve':
                # Create a new user for the student
                new_student = User.objects.create_user(
                    username=student.email,
                    email=student.email,
                    password=student.password,  
                    first_name=student.full_name.split()[0],
                    last_name=" ".join(student.full_name.split()[1:])
                )
                new_student.save()

                # Add the student to the 'Student' group
                student_group, created = Group.objects.get_or_create(name="Student")
                new_student.groups.add(student_group)

                # Save the student class in the profile
                StudentProfile.objects.create(user=new_student, student_class=student.student_class)

                # Send approval email
                subject = 'Application Approved'
                html_content = render_to_string('application_approved.html', {'user': student})
                text_content = strip_tags(html_content)
                from_email = f'Bwave ICT <{settings.EMAIL_HOST_USER}>'
                recipient_list = [student.email]

                msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # Remove from PendingStudent
                student.delete()
                messages.success(request, f"Student {student.full_name} approved successfully and notified via email.")

            elif action == 'delete':
                # Send rejection email
                subject = 'Application Rejected'
                html_content = render_to_string('application_rejected.html', {'user': student})
                text_content = strip_tags(html_content)
                from_email = f'Bwave ICT <{settings.EMAIL_HOST_USER}>'
                recipient_list = [student.email]

                msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # Delete the pending student
                student.delete()
                messages.success(request, f"Student {student.full_name} rejected and removed from the database.")

        except PendingStudent.DoesNotExist:
            messages.error(request, "Student not found.")

    students = PendingStudent.objects.all()
    return render(request, 'admin_pending_students.html', {'pending_students': students})
