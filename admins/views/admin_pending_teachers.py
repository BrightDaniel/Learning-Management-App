from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User, Group
from teachers.models import PendingTeacher
from django.contrib.auth.hashers import make_password

@login_required
def admin_pending_teachers(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        action = request.POST.get('action')

        try:
            teacher = PendingTeacher.objects.get(id=teacher_id)

            if action == 'approve':
                # Create a new user for the teacher
                new_teacher = User(
                    username=teacher.email,
                    email=teacher.email,
                    first_name=teacher.full_name.split()[0],
                    last_name=" ".join(teacher.full_name.split()[1:]),
                    is_staff=True
                )
                # Set the password directly since it's already hashed
                new_teacher.password = teacher.password
                new_teacher.save()

                # Add the teacher to the 'Teacher' group
                teacher_group, created = Group.objects.get_or_create(name="Teacher")
                new_teacher.groups.add(teacher_group)

                # Send approval email
                subject = 'Application Approved'
                html_content = render_to_string('application_approved.html', {'user': teacher})
                text_content = strip_tags(html_content)
                from_email = f'Bwave ICT <{settings.EMAIL_HOST_USER}>'
                recipient_list = [teacher.email]

                msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # Remove from PendingTeacher
                teacher.delete()
                messages.success(request, f"Teacher {teacher.full_name} approved successfully and notified via email.")

            elif action == 'delete':
                # Send rejection email
                subject = 'Application Rejected'
                html_content = render_to_string('application_rejected.html', {'user': teacher})
                text_content = strip_tags(html_content)
                from_email = f'Bwave ICT <{settings.EMAIL_HOST_USER}>'
                recipient_list = [teacher.email]

                msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # Delete the pending teacher
                teacher.delete()
                messages.success(request, f"Teacher {teacher.full_name} rejected and removed from the database.")

        except PendingTeacher.DoesNotExist:
            messages.error(request, "Teacher not found.")

    teachers = PendingTeacher.objects.all()
    return render(request, 'admin_pending_teachers.html', {'pending_teachers': teachers})