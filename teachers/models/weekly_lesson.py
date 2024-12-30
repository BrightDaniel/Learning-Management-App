from django.db import models
from .courses import Course
from cloudinary_storage.storage import RawMediaCloudinaryStorage

class WeeklyLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='weekly_lessons')
    week_name = models.CharField(max_length=100)
    content_file = models.FileField(
        upload_to='weekly_lessons/',
        storage=RawMediaCloudinaryStorage(),
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


class WeeklyQuiz(models.Model):
    weekly_lesson = models.OneToOneField(WeeklyLesson, on_delete=models.CASCADE, related_name='quiz')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_score(self):
        return sum(question.score for question in self.questions.all())

    def __str__(self):
        return f"Quiz for {self.weekly_lesson.week_name}"


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(WeeklyQuiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')]
    )
    score = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.question_text

    quiz = models.ForeignKey(WeeklyQuiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')]
    )
    score = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question_text