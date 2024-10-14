from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_habit, name='create_habit'),
    path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('habit/<int:habit_id>/', views.habit_detail, name='habit_detail'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('progress/', views.progress, name='progress'),
]