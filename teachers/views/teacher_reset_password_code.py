from django.shortcuts import render, redirect
from django.contrib import messages

def teacher_reset_password_code(request):
    if request.method == 'POST':
        entered_code = "".join(request.POST.getlist('code'))
        reset_code = request.session.get('reset_code')

        if entered_code == reset_code:
            messages.success(request, "Code verified successfully.")
            return redirect('teacher_reset_password')
        else:
            messages.error(request, "Invalid reset code.")
            return redirect('teacher_reset_password_code')

    return render(request, 'teacher_reset_password_code.html')
