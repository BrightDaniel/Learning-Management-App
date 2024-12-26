from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.conf import settings
from teachers.models import Class
from ..models import PendingStudent
from django.contrib.auth.models import User


def student_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        student_class_id = request.POST.get('class')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('student_register')

        # Check if email already exists in PendingStudent or User
        if PendingStudent.objects.filter(email=email).exists():
            messages.error(request, "This email is already pending approval.")
            return redirect('student_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('student_register')

        try:
            student_class = Class.objects.get(id=student_class_id)
        except Class.DoesNotExist:
            messages.error(request, "Invalid class selection.")
            return redirect('student_register')

        # Save to PendingStudent
        hashed_password = make_password(password)
        PendingStudent.objects.create(
            full_name=full_name,
            email=email,
            password=hashed_password,
            student_class=student_class
        )

        # Send verification email
        send_mail(
            'Student Registration Pending',
            f'Hello {full_name},\n\nYour registration is pending admin approval. You will receive another email once approved.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

        messages.success(request, "Registration successful. Check your email for further updates.")
        return redirect('student_register')

    classes = Class.objects.all()
    return render(request, 'student_register.html', {'classes': classes})