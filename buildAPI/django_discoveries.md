# Django Models 

## Primary Keys
For every model, Django automatically adds a primary key field called **`id`** unless you tell it otherwise.

So your model is effectively:

```python
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
```

### How tasks are uniquely identified
- **`id`** is:
  - An integer
  - Auto-incrementing
  - Unique
  - The **primary key**

You can access it like:

```python
task.id
```

or generically:

```python
task.pk
```

(`pk` is Django’s alias for “primary key” and works even if you rename it later.)

### When this is enough
For most apps, the default `id` is:
- Perfectly fine
- Fast
- Database-friendly
- What Django expects everywhere (URLs, admin, relations, etc.)

### If you want a different kind of unique identifier
Only do this if you have a real need (public APIs, security, syncing across systems, etc.).

#### Example: UUID instead of integer ID
```python
import uuid

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
```

This gives you IDs like:
```
550e8400-e29b-41d4-a716-446655440000
```
