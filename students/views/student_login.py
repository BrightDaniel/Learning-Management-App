from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


def student_login(request):
  
    if request.method == 'POST':
        email = request.POST.get('email_or_username')
        password = request.POST.get('password')

        # Authenticate the student
        user = authenticate(request, username=email, password=password)
        user = User.objects.get(email=email)
        print(User.objects.filter(email=email))
        print(user.is_active)

        
        if user:
            # Check if the user is in the 'Student' group
            if user.groups.filter(name='Student').exists():
                login(request, user)
                messages.success(request, "Login successful. Welcome to the Student Dashboard!")
                return redirect('student_dashboard')  
            else:
                messages.error(request, "Access denied! Only students can log in here.")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
        
    return render(request, 'student_login.html')