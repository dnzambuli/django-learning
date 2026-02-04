from rest_framework import serializers # convert model instances to and from JSON, so they can be sent over the web.
from .models import Task

# is a shortcut that automatically handles most things based on your model
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__' # include every field in the model