from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Class

def teacher_edit_class(request, class_id):
    # Ensure only teachers can access and fetch the class
    if not request.user.groups.filter(name='Teacher').exists():
        messages.error(request, "Access denied! Only teachers can edit classes.")
        return redirect('teacher_dashboard')

    class_instance = get_object_or_404(Class, id=class_id, teacher=request.user)

    if request.method == 'POST':
        if 'delete_class' in request.POST:
            # Delete class
            class_instance.delete()
            messages.success(request, f"Class '{class_instance.name}' deleted successfully!")
            return redirect('teacher_manage_class')
        else:
            # Edit class details
            class_name = request.POST.get('class_name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            description = request.POST.get('description')

            # Update class details
            class_instance.name = class_name
            class_instance.start_date = start_date
            class_instance.end_date = end_date
            class_instance.description = description
            class_instance.save()

            messages.success(request, "Class details updated successfully!")
            return redirect('teacher_manage_class')

    return render(request, 'teacher_edit_class.html', {'class_instance': class_instance})
