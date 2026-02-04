from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer


class TaskListCreate(generics.ListCreateAPIView):
    """
    Handles GET requests to list all tasks.
    Handles POST requests to create new tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles GET for one task, PUT/PATCH for updating, and DELETE to remove a task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


