from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    number = models.AutoField(primary_key=True)  # Автоматическое поле с уникальным значением
    title = models.CharField(max_length=200)     # Название задачи
    description = models.TextField(blank=True)   # Описание задачи
    assign = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')  # Назначенный пользователь задачи
    completed = models.BooleanField(default=False)  # Статус завершения задачи
    approved = models.BooleanField(default=False)  # Статус подтверждения завершения задачи

    def __str__(self):
        return self.title