from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import Group

def teacher_login(request):
    if request.method == 'POST':
        email = request.POST.get('email_or_username')
        password = request.POST.get('password')

        # Authenticate the teacher
        user = authenticate(request, username=email, password=password)
        
        if user:
            # Check if the user is in the 'Teacher' group
            if user.groups.filter(name='Teacher').exists():
                login(request, user)
                messages.success(request, "Login successful. Welcome to the Teacher Dashboard!")
                return redirect('teacher_dashboard')  
            else:
                messages.error(request, "Your account is not approved yet. Please contact the admin.")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
        
    return render(request, 'teacher_login.html')
