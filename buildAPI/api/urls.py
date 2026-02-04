from django.urls import path
from .views import TaskListCreate, TaskDetail, task_view

urlpatterns = [
    path('tasks/', task_view, name='task-list'), # The route to access or create tasks.
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'), # The route to get, update, or delete a single task by its primary key (pk).
]
