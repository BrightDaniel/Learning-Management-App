from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from teachers.models import WeeklyLesson, WeeklyQuiz
from ..models import QuizSubmission
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def start_quiz(request, week_id):
    weekly_lesson = get_object_or_404(WeeklyLesson, id=week_id)
    quiz = getattr(weekly_lesson, 'quiz', None)

    if not quiz:
        messages.error(request, "Quiz not available for this lesson.")
        return redirect('course_detail', course_id=weekly_lesson.course.id, week_id=week_id)

    # Check if user has already taken the quiz
    user_has_taken_quiz = QuizSubmission.objects.filter(user=request.user, quiz=quiz).exists()

    questions = quiz.questions.all()
    return render(request, 'start_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'user_has_taken_quiz': user_has_taken_quiz,
    })


@login_required
def submit_quiz(request):
    if request.method == "POST":
        week_id = request.POST.get('week_id')
        answers = {key.replace('answer-', ''): value for key, value in request.POST.items() if key.startswith('answer-')}

        weekly_lesson = get_object_or_404(WeeklyLesson, id=week_id)
        quiz = getattr(weekly_lesson, 'quiz', None)
        if not quiz:
            messages.error(request, "Quiz not available.")
            return redirect('course_detail', course_id=weekly_lesson.course.id, week_id=week_id)


        # Check if user has already submitted
        if QuizSubmission.objects.filter(user=request.user, quiz=quiz).exists():
            messages.error(request, "You have already submitted this quiz.")
            return redirect('course_detail', course_id=weekly_lesson.course.id, week_id=week_id)

        questions = quiz.questions.all()
        total_score = 0
        max_score = sum(question.score for question in questions)

        for question in questions:
            selected_answer = answers.get(str(question.id))
            if selected_answer and selected_answer == question.correct_answer:
                total_score += question.score

        # Save submission
        QuizSubmission.objects.create(user=request.user, quiz=quiz, score=total_score)

        # Flash message and redirect
        messages.success(request, f"Quiz successfully completed! Your score: {total_score}/{max_score}.")
        # return redirect('course_detail', course_id=weekly_lesson.course.id)
        return redirect('course_detail', course_id=weekly_lesson.course.id, week_id=week_id)



