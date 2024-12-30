from teachers.models import Course

def student_context(request):
    if request.user.is_authenticated and request.user.groups.filter(name="Student").exists():
        student_profile = getattr(request.user, 'profile', None)
        student_class = getattr(student_profile, 'student_class', None)

        # Fetch courses for the student's class
        courses = (
            Course.objects.filter(associated_class=student_class)
            .prefetch_related('weekly_lessons__quiz') if student_class else []
        )

        return {
            "student_name": request.user.get_full_name() or request.user.username,
            "student_email": request.user.email,
            "student_courses": courses,
        }
    return {}
