from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Task
from .forms import TaskForm

# Функия фильтрации по группам
def user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

# Фунция доступа к доскам, если пользователь авторизован
@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

# Представление для менеджеров (имеет доступ к управлению задачами)
@login_required
@user_passes_test(lambda u: user_in_group(u, "managers"), login_url='/forbidden/')
def managers_dashboard(request):
    tasks = Task.objects.all()
    return render(request, 'dashboard/managers.html', {'tasks': tasks})

# Представление для работников
@login_required
@user_passes_test(lambda u: user_in_group(u, "workers"), login_url='/forbidden/')
def workers_dashboard(request):
    incomplete_tasks = Task.objects.filter(completed=False)

    # Кнопка заверешения задачи
    if request.method == 'POST':
        task_number = request.POST.get('task_number')
        try:
            task = Task.objects.get(number=task_number)
            task.completed = True
            task.save()
        except Task.DoesNotExist:
            pass

    return render(request, 'dashboard/workers.html', {'tasks': incomplete_tasks})

# Представление для утверждающих
@login_required
@user_passes_test(lambda u: user_in_group(u, "approvers"), login_url='/forbidden/')
def approvers_dashboard(request):
    unapproved_tasks = Task.objects.filter(completed=True, approved=False)

    # Кнопка утверждения
    if request.method == 'POST':
        task_number = request.POST.get('task_number')
        try:
            task = Task.objects.get(number=task_number)
            task.approved = True
            task.save()
            return redirect('approvers_dashboard')  # Перенаправление после выполнения
        except Task.DoesNotExist:
            pass

    return render(request, 'dashboard/approvers.html', {'tasks': unapproved_tasks})

# Функция создания задачи
@login_required
@user_passes_test(lambda u: user_in_group(u, "managers"), login_url='/forbidden/')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('managers_dashboard')
    else:
        form = TaskForm(user=request.user)

    tasks = Task.objects.all()

    return render(request, 'dashboard/create_task.html', {'form': form, 'tasks': tasks})


# Редирект на страницу блокировки
def custom_permission_denied_view(request):
    return render(request, 'forbidden.html', status=403)
