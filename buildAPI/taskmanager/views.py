from rest_framework import viewsets, permissions
from .models import Task, CustomUser
from .serializers import TaskSerializer, CustomUserSerializer

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  # allow any user to access the API, authentication will be handled by djoser

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  # return only tasks that belong to the authenticated user
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)  # set the user field to the authenticated user when creating a new task

