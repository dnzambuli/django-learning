from django.db import models

# Create your models here.
class Task(models.Model):
    """
    Task table with:
        task_id
        task title - A short piece of text like "buy food"
        task completion status - boolean to mark task is done
    """
    title = models.CharField(max_length=200)
    completion = models.BooleanField(default=False)

    def __str__(self):
        """
        the string representation of a task
        :return:
        """
        return self.title
