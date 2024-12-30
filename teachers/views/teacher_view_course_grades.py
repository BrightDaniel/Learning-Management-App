from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..models import Course
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from students.models import QuizSubmission
from students.models import StudentProfile


@login_required
def teacher_view_course_grades(request):
    if not request.user.groups.filter(name='Teacher').exists():
        messages.error(request, "Access denied! Only teachers can access the dashboard.")
        return redirect('teacher_login')
    
    teacher = request.user  # Assumes the teacher is logged in
    courses = Course.objects.filter(teacher=teacher).select_related('associated_class')

    courses_with_student_counts = []
    for course in courses:
        # Count the number of students associated with the class
        student_count = StudentProfile.objects.filter(student_class=course.associated_class).count()
        courses_with_student_counts.append({
            'course': course,
            'class_name': course.associated_class.name,
            'student_count': student_count,
        })

    context = {'courses_with_student_counts': courses_with_student_counts}
    return render(request, 'teacher_view_course_grades.html', context)





def teacher_view_grade(request, course_id):
    teacher = request.user  # Assumes the teacher is logged in
    course = get_object_or_404(Course, id=course_id, teacher=teacher)

    # Fetch quiz submissions related to the course
    quiz_submissions = QuizSubmission.objects.filter(quiz__weekly_lesson__course=course).select_related('user', 'quiz__weekly_lesson')

    grades = []

    for submission in quiz_submissions:
        max_score = submission.quiz.total_score()
        status = "Passed" if submission.score >= 0.5 * max_score else "Failed"
        grades.append({
            'student_name': submission.user.get_full_name(),
            'student_email': submission.user.email,
            'week_name': submission.quiz.weekly_lesson.week_name,
            'score': submission.score,
            'max_score': max_score,
            'status': status,
        })

    context = {'course': course, 'grades': grades}
    return render(request, 'teacher_view_grade.html', context)
