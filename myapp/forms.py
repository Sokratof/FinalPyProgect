from django import forms
from .models import Task
from django.contrib.auth.models import User, Group

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['number', 'title', 'description', 'assign', 'completed', 'approved']

    # Назначить в поле можно только workers
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        workers_group = Group.objects.get(name='workers')
        self.fields['assign'].queryset = User.objects.filter(groups=workers_group)
