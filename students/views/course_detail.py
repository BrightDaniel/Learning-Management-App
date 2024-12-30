from django.shortcuts import render, redirect, get_object_or_404
from teachers.models import Course, WeeklyLesson
from ..models import QuizSubmission
from django.contrib import messages

def course_details(request, course_id):
    if not request.user.groups.filter(name="Student").exists():
        messages.error(request, "Access denied! Only students can access the dashboard.")
        return redirect("student_login")
    
    course = get_object_or_404(Course, id=course_id)
    weekly_lessons = course.weekly_lessons.all()
    
    context = {
        'course': course,
        'weekly_lessons': weekly_lessons,
    }
    return render(request, 'course_details.html', context)



def course_detail(request, course_id, week_id):
    if not request.user.groups.filter(name="Student").exists():
        messages.error(request, "Access denied! Only students can access the dashboard.")
        return redirect("student_login")

    course = get_object_or_404(Course, id=course_id)
    weekly_lesson = get_object_or_404(WeeklyLesson, id=week_id, course=course)
    quiz = getattr(weekly_lesson, 'quiz', None)

    # Check if the user has already taken the quiz
    user_has_taken_quiz = False
    if quiz:
        user_has_taken_quiz = QuizSubmission.objects.filter(user=request.user, quiz=quiz).exists()

    context = {
        'course': course,
        'weekly_lesson': weekly_lesson,
        'teacher_name': course.teacher.get_full_name(),
        'quiz': quiz,
        'user_has_taken_quiz': user_has_taken_quiz,
    }
    return render(request, 'course_detail.html', context)
