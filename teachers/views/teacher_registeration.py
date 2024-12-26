from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from ..models import PendingTeacher
from django.conf import settings


def teacher_registeration(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('teacher_registeration')

        # Check if email already exists in PendingTeacher or User
        if PendingTeacher.objects.filter(email=email).exists():
            messages.error(request, "This email is already pending approval.")
            return redirect('teacher_registeration')

        # Save to PendingTeacher
        hashed_password = make_password(password)
        PendingTeacher.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=hashed_password
        )

        # Send verification email
        send_mail(
            'Teacher Registration Pending',
            f'Hello {full_name},\n\nYour registration is pending admin approval. You will receive another email once approved.',
            settings.EMAIL_HOST_USER,  # Use email from settings
            [email],
            fail_silently=False
)

        messages.success(request, "Registration successful. Check your email for further updates.")
        return redirect('teacher_registeration')

    return render(request, 'teacher_registeration.html')
