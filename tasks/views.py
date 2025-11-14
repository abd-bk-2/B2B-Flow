from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Task, Business
from .forms import TaskForm


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = request.POST.get('business_name') or f"{user.username}'s Business"
            Business.objects.create(user=user, name=name)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def dashboard(request):
    business = request.user.business

    tasks = Task.objects.filter(creator=business) | Task.objects.filter(receiver=business)

    return render(request, 'dashboard.html', {'tasks': tasks})

@login_required
@require_http_methods(['GET', 'POST'])
def edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    business = request.user.business

    # only the creator may edit the task
    if task.creator != business:
        return HttpResponseForbidden('You do not have permission to edit this task.')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit.html', {'form': form, 'task': task})


@login_required
@require_http_methods(['GET', 'POST'])
def delete(request, pk):
    """On GET: render a confirmation page. On POST: perform the deletion.

    Only the task creator may delete the task.
    """
    task = get_object_or_404(Task, pk=pk)
    business = request.user.business
    if task.creator != business:
        return HttpResponseForbidden('You do not have permission to delete this task.')

    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')

    return render(request, 'confirm_delete.html', {'task': task})

@login_required
@require_http_methods(['GET', 'POST'])
def add_task(request):
    business = request.user.business

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.creator = business
            new_task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'form': form})