from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

@login_required
def all_users(request):
    if not request.user.is_superuser:
        return redirect('admin_login')

    # Query all users
    users = User.objects.all().order_by('-date_joined')

    # Paginate users
    paginator = Paginator(users, 20)  # 20 entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Paged object for template
    }
    return render(request, 'all_users.html', context)
