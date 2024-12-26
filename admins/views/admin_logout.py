from django.shortcuts import redirect
from django.contrib.auth import logout

def admin_logout(request):
    logout(request)
    return redirect('admin_login')  
