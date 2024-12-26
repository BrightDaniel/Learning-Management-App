from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Class

def teacher_create_class(request):
    # Ensure only teachers can access
    if not request.user.groups.filter(name='Teacher').exists():
        messages.error(request, "Access denied! Only teachers can create classes.")
        return redirect('teacher_login')

    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')

        # Check for unique class name
        if Class.objects.filter(name=class_name).exists():
            messages.error(request, "A class with this name already exists.")
        else:
            # Create the class and assign it to the logged-in teacher
            new_class = Class.objects.create(
                name=class_name,
                teacher=request.user,
                start_date=start_date,
                end_date=end_date,
                description=description
            )
            messages.success(request, f"Class '{new_class.name}' created successfully!")
            return redirect('teacher_dashboard')

    return render(request, 'teacher_create_class.html')
