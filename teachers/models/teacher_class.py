from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique class name
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_classes')  
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
