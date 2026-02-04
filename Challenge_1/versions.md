# Models

```python
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"username is: {self.username}\nfirst name is {self.fname}\nlast name is {self.lname}"

class Project (models.Model):
    STATUS_TODO = 'TODO'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_DONE = 'DONE'

    STATUS_CHOICES = [
        (STATUS_TODO, 'To Do'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_DONE, 'Done'),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    lead_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_TODO
    )

    def __str__(self):
        return f"Project: {self.title}\n======\nAbout Project\n======\n{self.description}"


class ProjectLabel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    color = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^#([A-Fa-f0-9]{6})$',
                message='Color must be a valid hex code like #RRGGBB'
            )
        ]
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    HIGH_PRIORITY = 'HIGH_PRIORITY'
    MEDIUM_PRIORITY = 'MEDIUM_PRIORITY'
    LOW_PRIORITY = 'LOW_PRIORITY'
    OPTIONAL_TASK = 'OPTIONAL_TASK'

    PRIORITY_CHOICES = [
        (HIGH_PRIORITY, 'High priority'),
        (MEDIUM_PRIORITY, 'Medium priority'),
        (LOW_PRIORITY, 'Low priority'),
        (OPTIONAL_TASK, 'Optional task'),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=OPTIONAL_TASK,
    )
    is_archived = models.BooleanField(default=False)

class TaskAttachment(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100)
    filetype = models.CharField(max_length=100)
    filepath = models.CharField(max_length=100)
    filesize = models.IntegerField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField()

    def __str__(self):
        return self.filename

class TaskNotification(models.Model):
    id = models.AutoField(primary_key=True)
    send_to = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_date = models.DateTimeField()

    def __str__(self):
        return self.message

class TaskComment(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.posted_by} commented on {self.task}\n\n{self.content}"

class TaskHistory(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.end_time} - {self.start_time}"

class Type(models.Model): # combined label with type
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class TaskTypeMap(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.icon
```