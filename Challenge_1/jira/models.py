from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    AbstractUser already provides: username, password, email, first_name, last_name,
    is_staff, is_active, date_joined, last_login
    """
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"


class Project(models.Model):
    """Project model representing a  project"""
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
    key = models.CharField(max_length=10, unique=True, help_text="Project key (e.g., PROJ)")
    description = models.TextField()
    lead_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='led_projects'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_TODO
    )
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created']

    def __str__(self):
        return f"{self.key}: {self.title}"


class ProjectMember(models.Model):
    """Represents team members in a project with their roles"""
    ROLE_ADMIN = 'ADMIN'
    ROLE_DEVELOPER = 'DEVELOPER'
    ROLE_VIEWER = 'VIEWER'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_DEVELOPER, 'Developer'),
        (ROLE_VIEWER, 'Viewer'),
    ]

    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_DEVELOPER)
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Project Member'
        verbose_name_plural = 'Project Members'
        unique_together = ('project', 'user')
        ordering = ['project', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.project.key} ({self.get_role_display()})"


class Sprint(models.Model):
    """Sprint/Iteration model for agile project management"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sprints')
    goal = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'
        ordering = ['-start_date']
        unique_together = ('project', 'name')

    def __str__(self):
        return f"{self.project.key} - {self.name}"


class Label(models.Model):
    """Labels/tags that can be applied to Projects"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    color = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^#([A-Fa-f0-9]{6})$',
                message='Color must be a valid hex code like #RRGGBB'
            )
        ],
        default='#0052CC'
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='labels')

    class Meta:
        verbose_name = 'Label'
        verbose_name_plural = 'Labels'
        unique_together = ('project', 'name')
        ordering = ['project', 'name']

    def __str__(self):
        return f"{self.project.key} - {self.name}"


class Task(models.Model):
    """Main task/issue model"""
    # Task Types
    TYPE_EPIC = 'EPIC'
    TYPE_STORY = 'STORY'
    TYPE_TASK = 'TASK'
    TYPE_BUG = 'BUG'
    TYPE_SUBTASK = 'SUBTASK'

    TYPE_CHOICES = [
        (TYPE_EPIC, 'Epic'),
        (TYPE_STORY, 'Story'),
        (TYPE_TASK, 'Task'),
        (TYPE_BUG, 'Bug'),
        (TYPE_SUBTASK, 'Subtask'),
    ]

    # Task Status
    STATUS_TODO = 'TODO'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_IN_REVIEW = 'IN_REVIEW'
    STATUS_DONE = 'DONE'

    STATUS_CHOICES = [
        (STATUS_TODO, 'To Do'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_IN_REVIEW, 'In Review'),
        (STATUS_DONE, 'Done'),
    ]

    # Task Priority
    PRIORITY_CRITICAL = 'CRITICAL'
    PRIORITY_HIGH = 'HIGH'
    PRIORITY_MEDIUM = 'MEDIUM'
    PRIORITY_LOW = 'LOW'

    PRIORITY_CHOICES = [
        (PRIORITY_CRITICAL, 'Critical'),
        (PRIORITY_HIGH, 'High'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_LOW, 'Low'),
    ]

    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=20, unique=True, help_text="Task key (e.g., PROJ-123)")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_TASK)

    # Relationships
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    parent_task = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subtasks'
    )
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    # Users
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )
    watchers = models.ManyToManyField(User, related_name='watched_tasks', blank=True)

    # Labels
    labels = models.ManyToManyField(Label, related_name='tasks', blank=True)

    # Status and Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)

    # Estimation and tracking
    story_points = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    estimated_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    # Dates
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    # Flags
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['sprint']),
        ]

    def __str__(self):
        return f"{self.key}: {self.title}"


class TaskComment(models.Model):
    """Comments on tasks"""
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='task_comments')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    class Meta:
        verbose_name = 'Task Comment'
        verbose_name_plural = 'Task Comments'
        ordering = ['created']

    def __str__(self):
        return f"{self.posted_by.username} on {self.task.key}: {self.content[:50]}"


class TaskAttachment(models.Model):
    """File attachments for tasks"""
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_attachments/')
    filename = models.CharField(max_length=255)
    filetype = models.CharField(max_length=100)
    filesize = models.BigIntegerField(help_text="File size in bytes")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Task Attachment'
        verbose_name_plural = 'Task Attachments'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.filename} ({self.task.key})"


class TaskHistory(models.Model):
    """Audit trail for task changes"""
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='task_changes')
    field_changed = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Task History'
        verbose_name_plural = 'Task Histories'
        ordering = ['-changed_at']
        indexes = [
            models.Index(fields=['task', '-changed_at']),
        ]

    def __str__(self):
        return f"{self.task.key}: {self.field_changed} changed by {self.user.username}"


class TimeLog(models.Model):
    """Time tracking for tasks"""
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='time_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='time_logs')
    hours_logged = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    description = models.TextField(blank=True)
    date_logged = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Time Log'
        verbose_name_plural = 'Time Logs'
        ordering = ['-date_logged']

    def __str__(self):
        return f"{self.user.username} - {self.hours_logged}h on {self.task.key}"


class Notification(models.Model):
    """User notifications"""
    TYPE_TASK_ASSIGNED = 'TASK_ASSIGNED'
    TYPE_TASK_UPDATED = 'TASK_UPDATED'
    TYPE_TASK_COMMENTED = 'TASK_COMMENTED'
    TYPE_TASK_MENTIONED = 'TASK_MENTIONED'
    TYPE_TASK_DUE = 'TASK_DUE'

    TYPE_CHOICES = [
        (TYPE_TASK_ASSIGNED, 'Task Assigned'),
        (TYPE_TASK_UPDATED, 'Task Updated'),
        (TYPE_TASK_COMMENTED, 'Task Commented'),
        (TYPE_TASK_MENTIONED, 'Mentioned in Task'),
        (TYPE_TASK_DUE, 'Task Due Soon'),
    ]

    id = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    message = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
        ]

    def __str__(self):
        return f"{self.get_notification_type_display()} for {self.recipient.username}"


