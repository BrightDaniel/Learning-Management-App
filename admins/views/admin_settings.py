from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def admin_settings(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    if request.method == 'POST':
        # Retrieve form data
        email = request.POST.get('email')
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Update email
        if email and email != user.email:
            user.email = email

        # Update username
        if username and username != user.username:
            user.username = username

        # Handle password change
        if old_password or new_password or confirm_password:
            if not user.check_password(old_password):
                messages.error(request, 'Old password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New password and confirm password do not match.')
            elif len(new_password) < 8:
                messages.error(request, 'New password must be at least 8 characters long.')
            else:
                user.set_password(new_password)
                update_session_auth_hash(request, user)  # Keep user logged in after password change
                messages.success(request, 'Password updated successfully.')

        # Save changes
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('admin_settings')

    # Pass current user details to the form
    context = {
        'email': request.user.email,
        'username': request.user.username,
    }
    return render(request, 'admin_settings.html', context)
