import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from teachers.models import PendingTeacher

def teacher_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            # Check if the user is a teacher
            if user.groups.filter(name="Teacher").exists():
                # Generate a reset code
                reset_code = str(random.randint(100000, 999999))

                # Save reset code to session or database (session used here for simplicity)
                request.session['reset_code'] = reset_code
                request.session['email'] = email

                # Send reset code via email
                send_mail(
                    'Password Reset Code',
                    f'Your password reset code is {reset_code}.',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                messages.success(request, "A reset code has been sent to your email.")
                return redirect('teacher_reset_password_code')
            else:
                messages.error(request, "This email does not belong to a registered teacher.")
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
        return redirect('teacher_forgot_password')

    return render(request, 'teacher_forgot_password.html')
