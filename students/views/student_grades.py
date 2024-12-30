from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import QuizSubmission


@login_required
def student_grades(request):
    # Ensure only students can access
    if not request.user.groups.filter(name="Student").exists():
        messages.error(request, "Access denied! Only students can access the dashboard.")
        return redirect("student_login")

    # Fetch the grades for the logged-in student
    submissions = QuizSubmission.objects.filter(user=request.user).select_related('quiz__weekly_lesson__course')
    grades = []

    for submission in submissions:
        max_score = submission.quiz.total_score()
        status = "Passed" if submission.score >= 0.5 * max_score else "Failed"
        grades.append({
            "course_name": submission.quiz.weekly_lesson.course.name,
            "week_name": submission.quiz.weekly_lesson.week_name,
            "score": submission.score,
            "max_score": max_score,
            "status": status,
        })

    return render(request, 'student_grades.html', {"grades": grades})
