from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            # Log in the user
            login(request, user)
            return redirect('admin_dashboard')  
        else:
            messages.error(request, "Invalid credentials or you are not authorized.")

    return render(request, 'admin_login.html')
