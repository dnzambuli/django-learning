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

You generally **should not include user passwords in your serializer output** because it creates serious security risks. Here’s why:

---

## 1. Security: You Must Never Expose Passwords

Passwords should **never be returned in API responses** — not even hashed ones.

If your serializer returns a password field:

- It could be exposed in API responses
- Logged in frontend consoles
- Stored in browser memory
- Captured in network logs
- Leaked through debugging tools

Even **hashed passwords** must not be exposed. While hashing algorithms like bcrypt are one-way, exposing hashes still:

- Gives attackers material for brute-force attacks
- Creates unnecessary risk if your database is ever compromised

---

## 2. Violates Basic Security Principles

Including passwords breaks:

- Principle of Least Privilege – clients don’t need passwords back
- Data Minimization – only send what’s necessary
- Zero Trust principles

Once a password is stored, your system should **never need to read it back** — only verify it.

---

## 3. It Encourages Bad Architecture

If you're tempted to serialize passwords, it often means:

- You're misunderstanding authentication flow
- You're treating passwords as normal fields
- You're not separating write-only vs read-only fields properly

In frameworks like:

- **Django REST Framework** → use `write_only=True`
- **Ruby on Rails** → use `has_secure_password`
- **Laravel** → hide with `$hidden`
- **Express.js** → never return it in JSON responses

Correct pattern example (DRF):

```python
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
```

---

## 4. Compliance & Legal Risk

Exposing passwords can violate:

- GDPR
- HIPAA
- PCI-DSS
- SOC 2 controls

That’s not just bad practice — it can be legally dangerous.

---

## 5. Authentication Should Work Like This

Correct flow:

1. User sends password → server
2. Server hashes & stores it
3. On login → compare hashed values
4. Return token (JWT/session)
5. Never return the password again

---

## The Golden Rule

Passwords are `write-only`.
They should never be readable — even by your own API.
