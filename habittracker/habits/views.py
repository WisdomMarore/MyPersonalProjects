from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Habit, Task, Progress, UserProfile
from .forms import HabitForm, TaskForm
from datetime import timedelta
from django.utils import timezone

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habits/dashboard.html', {'habits': habits})

@login_required
def create_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'Habit created successfully!')
            return redirect('dashboard')
    else:
        form = HabitForm()
    return render(request, 'habits/create_habit.html', {'form': form})

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    messages.success(request, 'Habit deleted successfully!')
    return redirect('dashboard')

@login_required
def habit_detail(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    tasks = Task.objects.filter(habit=habit)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.habit = habit
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('habit_detail', habit_id=habit.id)
    else:
        form = TaskForm()
    return render(request, 'habits/habit_detail.html', {'habit': habit, 'tasks': tasks, 'form': form})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, habit__user=request.user)
    task.completed = True
    task.save()
    
    # Update progress
    progress, created = Progress.objects.get_or_create(
        user=request.user,
        habit=task.habit,
        date=timezone.now().date()
    )
    progress.completed = True
    progress.save()
    
    # Update user points and level
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.points += 10
    if profile.points >= profile.level * 100:
        profile.level += 1
        messages.success(request, f'Congratulations! You\'ve reached level {profile.level}!')
    profile.save()
    
    messages.success(request, 'Task completed successfully!')
    return redirect('habit_detail', habit_id=task.habit.id)

@login_required
def progress(request):
    habits = Habit.objects.filter(user=request.user)
    progress_data = {}
    active_habits_count = 0
    total_completion_rate = 0
    longest_streak = 0

    for habit in habits:
        habit_data = {}
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # Get progress for the last 30 days
        progress_list = Progress.objects.filter(
            user=request.user,
            habit=habit,
            date__gte=thirty_days_ago,
            date__lte=today
        ).order_by('-date')

        completed_days = progress_list.filter(completed=True).count()
        total_days = (today - thirty_days_ago).days + 1
        completion_rate = (completed_days / total_days) * 100

        # Calculate current streak
        current_streak = 0
        for progress in progress_list:
            if progress.completed:
                current_streak += 1
            else:
                break

        # Update longest streak if necessary
        longest_streak = max(longest_streak, current_streak)

        habit_data = {
            'current_streak': current_streak,
            'completion_rate': round(completion_rate, 1),
            'completed_days': completed_days,
            'total_days': total_days,
            'recent_progress': progress_list[:7]  # Keep the last 7 days of progress
        }

        progress_data[habit] = habit_data
        active_habits_count += 1
        total_completion_rate += completion_rate

    overall_completion_rate = round(total_completion_rate / active_habits_count if active_habits_count > 0 else 0, 1)

    context = {
        'progress_data': progress_data,
        'active_habits_count': active_habits_count,
        'overall_completion_rate': overall_completion_rate,
        'longest_streak': longest_streak,
    }

    return render(request, 'habits/progress.html', context)