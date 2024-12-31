from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Course, WeeklyLesson, Class, WeeklyQuiz, QuizQuestion
from django.http import JsonResponse


@login_required
def teacher_manage_courses(request):
    # Ensure only teachers can access
    if not request.user.groups.filter(name='Teacher').exists():
        messages.error(request, "Access denied! Only teachers can manage courses.")
        return redirect('teacher_dashboard')

    courses = Course.objects.filter(teacher=request.user)

    return render(request, 'teacher_manage_courses.html', {'courses': courses})


'''
@login_required
def edit_course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    weekly_lessons = WeeklyLesson.objects.filter(course=course)

    if request.method == "POST":
        if 'week_name' in request.POST: 
            week_name = request.POST['week_name']
            content_file = request.FILES['content_file']
            WeeklyLesson.objects.create(course=course, week_name=week_name, content_file=content_file)
            messages.success(request, "Weekly content added successfully!")
        else:  # Editing Course Details
            course.name = request.POST['course_name']
            course.description = request.POST['course_description']
            course.associated_class_id = request.POST['class_id']
            course.save()
            messages.success(request, "Course details updated successfully!")
        return redirect('edit_course_details', course_id=course.id)

    return render(request, 'edit_course_details.html', 
                  {'course': course, 'weekly_lessons': weekly_lessons, 'classes': Class.objects.all()}
                  )

'''

@login_required
def edit_course_details(request, course_id):
    # Fetch the course and ensure the logged-in teacher is its owner
    course = get_object_or_404(Course, id=course_id, teacher=request.user)

    # Fetch weekly lessons associated with the course
    weekly_lessons = WeeklyLesson.objects.filter(course=course)

    if request.method == "POST":
        if 'week_name' in request.POST: 
            # Add weekly content
            week_name = request.POST['week_name']
            content_file = request.FILES['content_file']
            WeeklyLesson.objects.create(course=course, week_name=week_name, content_file=content_file)
            messages.success(request, "Weekly content added successfully!")
        else:  # Editing Course Details
            # Validate class selection
            try:
                associated_class = Class.objects.get(id=request.POST['class_id'], teacher=request.user)
            except Class.DoesNotExist:
                messages.error(request, "Invalid class selection.")
                return redirect('edit_course_details', course_id=course.id)
            
            # Update course details
            course.name = request.POST['course_name']
            course.description = request.POST['course_description']
            course.associated_class = associated_class
            course.save()
            messages.success(request, "Course details updated successfully!")
        return redirect('edit_course_details', course_id=course.id)

    # Filter classes to only those created by the teacher
    classes = Class.objects.filter(teacher=request.user)

    return render(request, 'edit_course_details.html', {
        'course': course,
        'weekly_lessons': weekly_lessons,
        'classes': classes,
    })







@login_required
def edit_weekly_content(request, content_id):
    content = get_object_or_404(WeeklyLesson, id=content_id)

    # Fetch the quiz if it exists, otherwise set it to None
    quiz = WeeklyQuiz.objects.filter(weekly_lesson=content).first()

    if request.method == "POST":
        if 'create_quiz' in request.POST:
            # Create a quiz for the weekly content if it doesn't exist
            if not quiz:
                quiz = WeeklyQuiz.objects.create(weekly_lesson=content)
                messages.success(request, "Quiz created successfully!")
            return redirect('edit_weekly_content', content_id=content.id)

        if 'save_question' in request.POST:
            if not quiz:
                messages.error(request, "Quiz does not exist. Please create a quiz first.")
                return redirect('edit_weekly_content', content_id=content.id)

            # Add a question to the quiz
            question_text = request.POST.get('question_text')
            option_a = request.POST.get('option_a')
            option_b = request.POST.get('option_b')
            option_c = request.POST.get('option_c')
            option_d = request.POST.get('option_d')
            correct_answer = request.POST.get('correct_answer')
            score = int(request.POST.get('score', 1))

            QuizQuestion.objects.create(
                quiz=quiz,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_answer=correct_answer,
                score=score,
            )
            messages.success(request, "Question added successfully!")
            return redirect('edit_weekly_content', content_id=content.id)

   
    questions = quiz.questions.all() if quiz else []

    return render(request, 'edit_weekly_content.html', {
        'lesson': content,
        'quiz': quiz,
        'questions': questions,
    })





# @login_required
# def add_quiz_question(request, quiz_id):
#     quiz = get_object_or_404(WeeklyQuiz, id=quiz_id)

#     if request.method == "POST":
#         question_text = request.POST.get('question_text')
#         option_a = request.POST.get('option_a')
#         option_b = request.POST.get('option_b')
#         option_c = request.POST.get('option_c')
#         option_d = request.POST.get('option_d')
#         correct_answer = request.POST.get('correct_answer')
#         score = int(request.POST.get('score', 1))
        
#         # Get the next order number
#         next_order = quiz.questions.count() + 1
        
#         question = QuizQuestion.objects.create(
#             quiz=quiz,
#             question_text=question_text,
#             option_a=option_a,
#             option_b=option_b,
#             option_c=option_c,
#             option_d=option_d,
#             correct_answer=correct_answer,
#             score=score,
#             order=next_order
#         )
        
#         return JsonResponse({
#             "id": question.id,
#             "question_text": question_text,
#             "score": score,
#             "order": next_order
#         })

#     return JsonResponse({"error": "Invalid request"}, status=400)

# @login_required
# def publish_quiz(request, quiz_id):
#     quiz = get_object_or_404(WeeklyQuiz, id=quiz_id)

#     if request.method == "POST":
#         # Check if there are any saved questions
#         if quiz.questions.exists():
#             quiz.is_published = True
#             quiz.save()
#             messages.success(request, "Quiz published successfully!")
#         else:
#             messages.error(request, "Cannot publish quiz. Add at least one question first.")
#         return redirect('edit_weekly_content', content_id=quiz.weekly_lesson.id)

#     return JsonResponse({"error": "Invalid request"}, status=400)



@login_required
def delete_question(request, question_id):
    question = get_object_or_404(QuizQuestion, id=question_id)
    question.delete()
    return JsonResponse({"message": "Question deleted successfully!"})


def delete_weekly_content(request, content_id):
    content = get_object_or_404(WeeklyLesson, id=content_id)
    content.delete()
    messages.success(request, "Weekly content deleted successfully!")
    return redirect('edit_course_details', course_id=content.course.id)