from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def teacher_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('teacher_login') 
