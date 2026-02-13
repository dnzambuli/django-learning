from rest_framework import serializers
from .models import Task# , CustomUser

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__' # Get all fields from Task model
        read_only_fields = ['user'] # make user field read-only since it will be set to the authenticated user in the view

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email', 'profile_picture'] # specify fields to include in the serializer