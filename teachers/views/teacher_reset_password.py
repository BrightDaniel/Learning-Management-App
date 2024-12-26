from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def teacher_reset_password(request):
    email = request.session.get('email')

    if not email:
        messages.error(request, "Session expired. Please restart the password reset process.")
        return redirect('teacher_forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('teacher_reset_password')

        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()

            # Clear session data
            request.session.pop('reset_code', None)
            request.session.pop('email', None)

            messages.success(request, "Password reset successful. Please log in.")
            return redirect('teacher_login')
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return redirect('teacher_forgot_password')

    return render(request, 'teacher_reset_password.html')
