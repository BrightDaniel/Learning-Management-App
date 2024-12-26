from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def admin_manage_classes(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    return render(request, 'admin_manage_classes.html')
